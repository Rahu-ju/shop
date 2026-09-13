import weasyprint

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.staticfiles import finders
from django.http import HttpResponse
from django.template.loader import render_to_string

from .forms import AddressCreationForm
from .models import OrderItem, Order
from .task import order_created
from cart.cart import Cart

# Create your views here.

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = AddressCreationForm(request.POST)
        
        if form.is_valid():

            # create the address and save it to the database
            address = form.save(commit=False)
            if request.user.is_authenticated:
                address.user = request.user
            address.save()

            # create the order and save it to the database
            order = Order.objects.create(
                user=request.user if request.user.is_authenticated else None,
                address=address,
            )
            
            # Take each item from the cart and create the order item.
            for item in cart:
                OrderItem.objects.create(
                    order = order,
                    product = item['product'],
                    price = item['price'],
                    quantity = item['quantity']
                )
            
            #Clear the cart and send mail asynchronously
            cart.clear()
            order_created.delay(order.id)

            # set order id to session and then redirect to the payment process
            request.session['order_id'] = order.id

            template = 'templates/order-summary.html'
            context = {'order': order, }
            return render(request, template, context)
        
        else:
            # template can catch the error using form.error
            template = 'templates/checkout.html'
            context = {'form': form, 'cart': cart,}
            return render(request, template, context)

    else:
        if request.user.is_authenticated:
            address = request.user.address 
            form = AddressCreationForm(instance=address)
        else:
            form = AddressCreationForm()
        template = 'templates/checkout.html'
        context = {'form': form, 'cart': cart}
        return render(request, template, context)



def order_summary(request):
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    context = {'order': order}
    return render(request, 'templates/order-summary.html', context)


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    return render(request, 'admin/orders/order/order_detail.html', {'order': order})



@staff_member_required
def admin_order_pdf(request, order_id):

    # Retrive the order object and Render the template with necessary variables
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/order/pdf.html', {'order': order})

    # Find the css file
    css_file = finders.find('shop/css/pdf.css')

    # Feed it to WeasyPrint
    pdf = weasyprint.HTML(string=html).write_pdf(stylesheets=[weasyprint.CSS(filename=css_file)])

    # Return it as response
    response = HttpResponse(content=pdf, content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="order-{order.id}.pdf"'
    return response
