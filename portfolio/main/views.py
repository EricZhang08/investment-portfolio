from collections import namedtuple
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User, Stock
from .forms import RegistrationForm
# Create your views here.

def index(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user_pwd = form.cleaned_data['password']
            user_email = form.cleaned_data['email']
            user_name = form.cleaned_data['name']
            user = User(name=user_name, email=user_email, password=user_pwd)
            user.save()
            return redirect('index')
    else:
        form = RegistrationForm()
        return render(request, 'main/index.html', {
            'form': form
        })