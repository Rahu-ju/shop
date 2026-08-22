from django import forms

from .models import Order



class OrderCreationForm(forms.ModelForm):
    name = forms.CharField(max_length=100)
    class Meta:
        model = Order
        fields = [
            'email',
            'phone',
            'address',
            'postal_code',
            'city',
        ]

    def save(self, commit=True):
        order = super().save(commit=False)
        order.first_name = self.cleaned_data['name']
        order.last_name = ''
        if commit:
            order.save()
        return order
    
