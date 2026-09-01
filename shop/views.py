from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from .models import Category, Product
from cart.forms import  CartAddProductForm
from cart.cart  import Cart



def home(request):
    '''
    It will pull some 5 products as feature product.
    '''

    products = Product.objects.filter(available=True)
    sliders = products[:3]
    context = {'products': products, 'sliders': sliders}
    return render(request, 'templates/home.html', context)




def product_list(request, category_slug=None):
    ''' Retrieve all the category, and product. if category_slug is given,
       then retrieve all the product according to that category. '''

    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    context = {
        'category': category, 
        'categories': categories, 
        'products': products,
        }

    # template = 'shop/product/list.html'
    template = 'templates/products.html'

    return render(request, template, context)



def product_detail(request, id, slug):
    '''Show the detail info of a product.'''

    product = get_object_or_404(Product, id=id, slug=slug, available=True)

    cart = Cart(request)
    product_quantity = cart.get_product_quantity(id)

    cart_product_form = CartAddProductForm()

    context = {'product': product, 
               'cart_product_form': cart_product_form,
               'product_quantity': product_quantity}
    template = 'templates/product-detail.html'

    return render(request, template, context)



def dashboard(request):
    dashboard = None

    # render orders snipets
    if request.headers.get('HX-Request') and request.GET.get('order_tab'):
        html = 'templates/dashboard/orders.html'
        return render(request, html)

    # render address snipets
    if request.headers.get('HX-Request') and request.GET.get('address_tab'):
        html = 'templates/dashboard/address.html'
        return render(request, html)
    
    return render(request, 'templates/dashboard/overview.html', {'dashboard': dashboard} )

