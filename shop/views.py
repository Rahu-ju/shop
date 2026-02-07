from django.shortcuts import render, get_object_or_404

from .models import Category, Product
from cart.forms import  CartAddProductForm



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

    template = 'shop/product/list.html'

    return render(request, template, context)



def product_detail(request, id, slug):
    '''Show the detail info of a product.'''

    product = get_object_or_404(Product, id=id, slug=slug, available=True)

    cart_product_form = CartAddProductForm()

    context = {'product': product, 'cart_product_form': cart_product_form}
    template = 'shop/product/detail.html'

    return render(request, template, context)

