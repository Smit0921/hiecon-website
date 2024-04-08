from django import forms
from .models import Customer,User
from django.contrib.auth.forms import UserCreationForm
from .models import Newsletter


class CustomerRegistrationForm(UserCreationForm):
    name = forms.CharField(max_length=20)
    address = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=255, help_text='Required. Enter a valid email address.')
    mobile_no = forms.IntegerField()

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'name', 'address', 'email', 'mobile_no']
 

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    
class NewsletterSubscriptionForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = Newsletter
        fields = ['email']