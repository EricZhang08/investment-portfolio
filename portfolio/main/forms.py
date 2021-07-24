
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

class ViewForm(forms.Form):
    # def __init__(self, *args, **kwargs):
    #     super(ViewForm, self).__init__(*args, **kwargs)
    #     self.fields['name'].disabled = True
    # name = forms.CharField(widget=forms.TextInput, required=False )
    # percentage = forms.FloatField(required=False)
    def __init__(self, n , *args, **kwargs):
        super(ViewForm, self).__init__(*args, **kwargs)
        # selected_user = User.objects.filter(id=self.u_id)
        i = 1
        for temp in n:
            self.fields["company_name %d" % i] = forms.CharField(initial=temp.ticker)
            self.fields["percentage %d" % i] = forms.CharField()
            i+=1

