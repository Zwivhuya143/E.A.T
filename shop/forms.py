from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from shop.models import Product


class LoginForm(forms.Form):
    username = forms.CharField(max_length=65, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(max_length=65, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    

class RegisterForm(UserCreationForm):
    class Meta:
        model=User
        fields = ['username','email','password1','password2'] 
   
class CheckoutForm(forms.Form):
    first_name = forms.CharField(max_length=65)
    last_name = forms.CharField(max_length=65)
    address = forms.CharField(max_length=65)
    city = forms.CharField(max_length=65)
    state = forms.CharField(max_length=65)
    zip_code = forms.CharField(max_length=65)
    phone = forms.CharField(max_length=65)
    email = forms.CharField(max_length=65)

class ProductForm(forms.Form):
    class Meta:
        model = Product
        fields = ('category', 'product_id','name', 'description', 'price', 'image' )
        labels = {
            'category': '',
            'product_id': '',
            'name': '',
            'description': '',
            'price': '',
            'image':''
        }