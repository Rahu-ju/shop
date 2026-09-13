from django.db import models
from django.conf import settings



class Address(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=30)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)

    def __str__(self):
        return self.city
    



class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    address = models.ForeignKey(Address, related_name='orders', on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    paid = models.BooleanField(default=False)
    stripe_id = models.CharField(max_length=250, blank=True)
    bkash_trx_id = models.CharField(max_length=250, blank=True)


    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
            ]


    def __str__(self):
        return f'order {self.id}'


    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())
    

    def get_stripe_url(self):
        if not self.stripe_id:
            return ''
        
        if '_test_' in settings.STRIPE_SECRET_KEY:
            path = '/test/'
        else:
            path = '/'

        return f'https://dashboard.stripe.com{path}payments/{self.stripe_id}'



class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey('shop.Product', related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)


    def __str__(self):
        return str(self.id)


    def get_cost(self):
        return self.price * self.quantity

    
