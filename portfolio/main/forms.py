
from django import forms
from .models import *

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ('name', 'email', 'password')

class LoginForm(forms.Form):
    email = forms.EmailField(label='Your email')
    password = forms.CharField(widget=forms.PasswordInput)

class SearchForm(forms.Form):
    company_name = forms.CharField(widget= forms.TextInput
                           (attrs={'class':'form-control me-2',
				   'id':'myInput'}))