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
def get_user_address(user):
    return getattr(user, 'address', None) if user.is_authenticated else None

def order_create(request):
    cart = Cart(request)
    existing_address = get_user_address(request.user)

    if request.method == 'POST':
        form = AddressCreationForm(request.POST, instance=existing_address)

        if not form.is_valid():
            return render(request, 'templates/checkout.html', {'form': form, 'cart': cart})

        address = form.save(commit=False)
        if request.user.is_authenticated:
            address.user = request.user
        address.save()

        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            address=address,
        )

        OrderItem.objects.bulk_create([
            OrderItem(order=order, product=item['product'], price=item['price'], quantity=item['quantity'])
            for item in cart
        ])

        cart.clear()
        order_created.delay(order.id)
        request.session['order_id'] = order.id

        # return render(request, 'templates/order-summary.html', {'order': order})
        return redirect('orders:order_summary')

    initial = {}
    if not existing_address and request.user.is_authenticated:
        initial = {'name': request.user.username, 'email': request.user.email}

    form = AddressCreationForm(instance=existing_address, initial=initial)
    return render(request, 'templates/checkout.html', {'form': form, 'cart': cart})



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
