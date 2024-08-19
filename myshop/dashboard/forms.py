from django import forms
from products.models import Product
from accounts.models import SellerProfile

class SellerBankDetailsForm(forms.ModelForm):
    class Meta:
        model = SellerProfile
        fields = ['bank_account_number', 'bank_routing_number']
        widgets = {
            'bank_account_number': forms.TextInput(attrs={'class': 'form-control'}),
            'bank_routing_number': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'category', 'price', 'description', 'image', 'stock']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
        }
