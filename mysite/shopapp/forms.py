from django.contrib.auth.models import Group
from django import forms

from .models import Product, Order


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "name", "price", "description", "discount", "preview"
    images = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={"multile": True}),
    )


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = "delivery_address", "promocode", "user", "products"


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = "name",

class CSVImportForm(forms.Form):
    csv_file = forms.FileField()