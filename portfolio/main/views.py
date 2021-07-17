from collections import namedtuple
from datetime import date
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User, Stock, Ticker
from .forms import RegistrationForm, LoginForm, SearchForm
from requests_html import HTMLSession
import datetime
from datetime import timezone
from bs4 import BeautifulSoup
import json
import csv

class findData():
    def __init__(self):
        pass
    def find_html(self,ticker):
        session = HTMLSession()
        dt = datetime.datetime.today()
        dt = dt.replace(minute=00, hour=00, second=00)
        timestamp = int(dt.replace(tzinfo=timezone.utc).timestamp())
        five_year_before = timestamp - 60 * 60 *24 *365 * 5 - 60 * 60 *24

        url =  'https://finance.yahoo.com/quote/'+ticker+'/history?period1='+ str(five_year_before) +  '&period2=' + str(timestamp) + '&interval=1mo&filter=history&frequency=1mo&includeAdjustedClose=true'

        page = session.get(url)
        page.html.render()
        soup = BeautifulSoup(page.content, 'html.parser')

        table = soup.find( "table", {"data-test":"historical-prices"} )
        adj_close = list()
        for row in table.tbody.findAll("tr"):
            temp = row.findAll('td')
            if (len(temp)>6):
                adj_close.append(temp[5].text)
        return adj_close

    def find_ticker(self,company_name):
        with open('/Users/ding/investment-portfolio/portfolio/main/ticker.csv') as f:
            reader = csv.reader(f)
            for row in reader:
                _, created = Ticker.objects.get_or_create(
                    stock_name=row[1],
                    ticker=row[0],
                    )
        return Ticker.objects.get(stock_name=company_name).ticker
    
    def get_data(self,name):
        ticker = self.find_ticker(name)
        return self.find_html(ticker)

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
            if not selected_user.portfolio.filter(ticker=company):
                stock = Stock(ticker=company)
                stock.save()
                selected_user.portfolio.add(stock)
    # print(selected_user.email)
            # for stock in selected_user.portfolio.all():
            #     print(stock)
    
    search_form = SearchForm()
    return render(request, 'main/index.html', {
        'selected_user': selected_user,
        'search_form': search_form,
        'portfolio': selected_user.portfolio.all()
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

# def risk_parity(ticker):
#     x = findData()
#     print(x.get_data("Apple Inc. Common Stock"))


def calculate(request, user_id):
    selected_user = User.objects.get(id=user_id)
    x = findData()
    x.get_data('Agilent Technologies Inc. Common Stock')
    # data = x.get_data("Apple Inc. Common Stock")
    # print(data)
    return render(request, 'main/calculate.html', {
        'user_id': user_id,
        'selected_user': selected_user,
        'portfolio': selected_user.portfolio.all(),
        # 'data': data
    })

