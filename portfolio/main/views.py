from collections import namedtuple
from datetime import date
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import User, Stock, Ticker
from .forms import RegistrationForm, LoginForm, SearchForm, ViewForm
from requests_html import AsyncHTMLSession
import datetime
from datetime import timezone
from bs4 import BeautifulSoup
import json
import csv
import asyncio
import hashlib
from main import my_helpers


# def find_html(self,ticker):
#     session = HTMLSession()
#     dt = datetime.datetime.today()
#     dt = dt.replace(minute=00, hour=00, second=00)
#     timestamp = int(dt.replace(tzinfo=timezone.utc).timestamp())
#     five_year_before = timestamp - 60 * 60 *24 *365 * 5 - 60 * 60 *24

#     url =  'https://finance.yahoo.com/quote/'+ticker+'/history?period1='+ str(five_year_before) +  '&period2=' + str(timestamp) + '&interval=1mo&filter=history&frequency=1mo&includeAdjustedClose=true'

#     page = session.get(url)
#     page.html.render()
#     soup = BeautifulSoup(page.content, 'html.parser')

#     table = soup.find( "table", {"data-test":"historical-prices"} )
#     adj_close = list()
#     for row in table.tbody.findAll("tr"):
#         temp = row.findAll('td')
#         if (len(temp)>6):
#             adj_close.append(temp[5].text)
#     return adj_close

# def find_ticker(self,company_name):
#     with open('/Users/ding/investment-portfolio/portfolio/main/ticker.csv') as f:
#         reader = csv.reader(f)
#         for row in reader:
#             _, created = Ticker.objects.get_or_create(
#                 stock_name=row[1],
#                 ticker=row[0],
#                 )
#     return Ticker.objects.get(stock_name=company_name).ticker

# def get_data(self,name):
#     ticker = self.find_ticker(name)
#     return self.find_html(ticker)

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user_pwd = hashlib.md5(str(form.cleaned_data['password']).encode('utf-8')).hexdigest()
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
    val = selected_user.portfolio.all()
    form = SearchForm(request.POST or None)
    viewsform = ViewForm(val, request.POST or None, )
    # temp = {}
    # for stock in selected_user.portfolio.all():
    #     temp[stock.ticker] = ViewForm(initial={'name': stock.ticker})
    if request.method == 'POST':
        if form.is_valid():
            company = form.cleaned_data['company_name']
            if not selected_user.portfolio.filter(ticker=company):
                stock = Stock(ticker=company)
                stock.save()
                selected_user.portfolio.add(stock)
        # if viewsform.is_valid():
        #     print(viewsform.cleaned_data)
    
    search_form = SearchForm()

    

    
    return render(request, 'main/index.html', {
        'selected_user': selected_user,
        'search_form': search_form,
        'portfolio': selected_user.portfolio.all(),
        'view_form': viewsform
    })

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            user_pwd = hashlib.md5(str(form.cleaned_data['password']).encode('utf-8')).hexdigest()
  
            if User.objects.filter(email=user_email).exists():
                selected_user = User.objects.get(email=user_email)
                print(selected_user.password == user_pwd)
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
    portfolio = selected_user.portfolio.all()
    viewsform = ViewForm(portfolio, request.POST or None, )
    dict_adj = {}
    views_dict = {}
    for stock in portfolio:
        ticker = Ticker.objects.get(stock_name=stock.ticker).ticker
        dt = datetime.datetime.today()
        dt = dt.replace(minute=00, hour=00, second=00)
        timestamp = int(dt.replace(tzinfo=timezone.utc).timestamp())
        five_year_before = timestamp - 60 * 60 *24 *365 * 5 - 60 * 60 *24
        url =  'https://finance.yahoo.com/quote/'+ticker+'/history?period1='+ str(five_year_before) +  '&period2=' + str(timestamp) + '&interval=1mo&filter=history&frequency=1mo&includeAdjustedClose=true'
        
        async def get_post(url):
            new_loop=asyncio.new_event_loop()
            asyncio.set_event_loop(new_loop)
            session = AsyncHTMLSession()
            resp_page = await session.get(url)
            await resp_page.html.arender()
            await session.close()
            return resp_page
        
        page = resp = asyncio.run(get_post(url))

        soup = BeautifulSoup(page.content, 'html.parser')

        table = soup.find( "table", {"data-test":"historical-prices"} )
        
        adj_close = list()
        for row in table.tbody.findAll("tr"):
            temp = row.findAll('td')
            if (len(temp)>6):
                adj_close.append(float((temp[5].text).replace(',', '')))
        adj_close.reverse()
        if len(adj_close)>60:
            adj_close = adj_close[0:60]

        if len(adj_close)<60:
            return HttpResponse(str(stock.ticker) + " does not have enough data")
            
        dict_adj[stock.ticker] = adj_close
    # print(dict_adj)
    
    # data = x.get_data("Apple Inc. Common Stock")
    # print(data)
    if request.method == 'POST':
        # form = ViewForm(request.POST)
        if viewsform.is_valid():
            # print(viewsform.cleaned_data)
            views = viewsform.cleaned_data
            keys = list(views.keys())
            for i in range(0,len(keys)-1, 2):
                views_dict[views[keys[i]]] = float(views[keys[i+1]])
        bl = my_helpers.bl_portfolio(dict_adj, views_dict)
        print(bl)
    else:
        bl = my_helpers.bl_portfolio(dict_adj)
    risk_parity = my_helpers.risk_parity(dict_adj)
    mv = my_helpers.solver(dict_adj)
    return render(request, 'main/calculate.html', {
        'user_id': user_id,
        'selected_user': selected_user,
        'portfolio': selected_user.portfolio.all(),
        'risk_parity': risk_parity['weights'],
        'rp_keys': risk_parity['weights'].keys(),
        'ave_return': risk_parity['stats']['ave_return'],
        'portfolio_vol': risk_parity['stats']['portfolio_vol'],
        'weights_msr': mv['weights_msr'],
        'ret_msr': mv['stats_msr'][0],
        'vol_msr': mv['stats_msr'][1],
        'weights_min': mv['weights_min'],
        'ret_min': mv['stats_min'][0],
        'vol_min': mv['stats_min'][1],
        'bl_weights_msr': bl['weights_msr'],
        'bl_ret_msr': bl['stats_msr'][0],
        'bl_vol_msr': bl['stats_msr'][1],
        'bl_weights_min': bl['weights_min'],
        'bl_ret_min': bl['stats_min'][0],
        'bl_vol_min': bl['stats_min'][1],


        # 'data': data
    })

