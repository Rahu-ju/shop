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

            for item in cart:
                OrderItem.objects.create(
                    order = order,
                    product = item['product'],
                    price = item['price'],
                    quantity = item['quantity']
                )
            
            cart.clear()
            #initiate asynchronous task
            order_created.delay(order.id)


            template = 'orders/created.html'
            context = {'order': order, }
            return render(request, template, context)
        
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