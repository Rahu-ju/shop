from django.shortcuts import render

from .forms import OrderCreationForm
from .models import OrderItem
from .task import order_created
from cart.cart import Cart

# Create your views here.

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreationForm(request.POST)
        
        if form.is_valid():
            order = form.save()

            # Take each item from the cart and create the order item.
            for item in cart:
                OrderItem.objects.create(
                    order = order,
                    product = item['product'],
                    price = item['price'],
                    quantity = item['quantity']
                )
            
            #Clear the cart and initiate asynchronous task
            cart.clear()
            order_created.delay(order.id)

            # set order id to session and then redirect to the payment process
            request.session['order_id'] = order.id
            return redirect('payment:process')


            # template = 'orders/created.html'
            # context = {'order': order, }
            # return render(request, template, context)
        
        else:
            # template can catch the error using form.error
            template = 'orders/create.html'
            context = {'form': form, 'cart': cart,}
            return render(request, template, context)

    else:
        form = OrderCreationForm()
        template = 'orders/create.html'
        context = {'form': form, 'cart': cart}
        return render(request, template, context)