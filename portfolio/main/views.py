from collections import namedtuple
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User, Stock
from .forms import RegistrationForm, LoginForm, SearchForm
# Create your views here.

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user_pwd = form.cleaned_data['password']
            user_email = form.cleaned_data['email']
            user_name = form.cleaned_data['name']
            user = User(name=user_name, email=user_email, password=user_pwd)
            user.save()
            # print(user_email)
            return redirect('index', user_id=user.id)
    else:
        form = RegistrationForm()
        return render(request, 'main/register.html', {
            'form': form
        })
def index(request, user_id):
    selected_user = User.objects.get(id=user_id)
    form = SearchForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            company = form.cleaned_data['company_name']
            stock = Stock(ticker=company)
            stock.save()
            selected_user.portfolio.add(stock)
    # print(selected_user.email)
    search_form = SearchForm()
    return render(request, 'main/index.html', {
        'selected_user': selected_user,
        'search_form': search_form
    })

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            user_pwd = form.cleaned_data['password']
            if User.objects.filter(email=user_email).exists():
                selected_user = User.objects.get(email=user_email)
                if selected_user.password == user_pwd:
                    # return redirect('index', user_id=selected_user.id)
                    return index(request, selected_user.id)
                # need better authentication
    form = LoginForm()
    return render(request, 'main/login.html', {
        'message': 'sorry, your email or password is incorrect',
        'form': form,
    })


