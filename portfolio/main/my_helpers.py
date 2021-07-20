from datetime import date
from sys import displayhook
import numpy as np
# from numpy.core.fromnumeric import var
import pandas as pd
from pulp import * 
import random
from pypfopt import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns
from pypfopt.expected_returns import mean_historical_return
from pypfopt.risk_models import CovarianceShrinkage
from dateutil.relativedelta import relativedelta
import datetime
def risk_parity(dict_adj):
    ret = {}
    stdev = {}
    weights = {}
    total_std = 0
    ave_return = 0
    for key in dict_adj:
        adj_close = dict_adj[key]
        # adj_close.reverse()
        data = list()
        for i in range(len(adj_close)-2):
            monthly_return = adj_close[i+1]/adj_close[i] - 1
            data.append(monthly_return)
        ret[key] = data
    for key in ret:
        stdev[key] = np.std(ret[key], ddof=1)
        total_std+=1/stdev[key]
    for key in stdev:
        weights[key]=round(100*(1/stdev[key])/total_std, 2)
        ave_return+= round(np.average(ret[key])*weights[key], 2)
    portfolio_vol = get_portfolio_vol(ret, weights)
    stats = {'ave_return': ave_return, 'portfolio_vol': portfolio_vol}
    results = {'weights': weights, 'stats': stats}
    return results


def get_cov_matrix(returns_dict):
    ret_list = []
    for key in returns_dict:
        ret_list.append(returns_dict[key])
    return np.cov(ret_list, ddof=1)

def get_portfolio_vol(returns_dict, weights_dict):
    weights = []
    for key in weights_dict:
        weights.append(weights_dict[key])
    cov_matrix = get_cov_matrix(returns_dict)
    portfolio_var = np.matmul(weights, np.matmul(cov_matrix, weights))
    return round(np.sqrt(portfolio_var), 2)

def solver(dict_adj):
    ret = {}
    exp_ret = {}
    stdev = {}
    weights = {}
    for key in dict_adj:
        adj_close = dict_adj[key]
        # adj_close.reverse()
        data = list()
        for i in range(len(adj_close)-2):
            monthly_return = adj_close[i+1]/adj_close[i] - 1
            data.append(monthly_return)
        ret[key] = data
    for key in ret:
        stdev[key] = np.std(ret[key], ddof=1)
        exp_ret[key] = np.average(ret[key])
        weights[key] = random.random()
  
    # str_price = {}
    # str_data = list()
    # for key in dict_adj:
    #     for i in range(len(dict_adj[key])):
    #         str_data.append(str(dict_adj[key][i]))
    #     str_price[key] = str_data
    df_price = pd.DataFrame(dict_adj, columns=[key for key in dict_adj])
    dates = pd.date_range(datetime.datetime.now() - relativedelta(years=5),datetime.datetime.now(), 
              freq='MS').strftime("%Y-%m").tolist()
    # print(dates)
    df_price.insert(0, 'date', dates)
  
    # print(df_price)
    # mu = mean_historical_return(df_price)
    # S = CovarianceShrinkage(df_price).ledoit_wolf()
    

adj_close = {'Apple Inc. Common Stock': [24.78, 26.55, 26.66, 25.95, 27.34, 28.64, 32.33, 34.05, 34.05, 36.21, 34.28, 35.4, 39.04, 36.83, 40.39, 41.06, 40.58, 40.15, 42.72, 40.4, 39.79, 45.0, 44.74, 46.0, 55.02, 54.76, 53.09, 43.32, 38.4, 40.51, 42.15, 46.43, 49.06, 42.8, 48.57, 52.28, 51.22, 55.17, 61.28, 65.83, 72.55, 76.47, 67.54, 62.98, 72.76, 78.74, 90.59, 105.55, 128.18, 115.24, 108.33, 118.47, 132.27, 131.54, 120.87, 121.94, 131.24, 124.4, 136.96, 146.39], 
'Agilent Technologies Inc. Common Stock': [45.0, 45.11, 41.84, 42.23, 43.75, 47.16, 49.41, 50.92, 53.15, 58.26, 57.26, 57.85, 62.62, 62.12, 65.83, 67.14, 64.94, 71.36, 66.65, 65.01, 63.88, 60.31, 60.23, 64.32, 65.94, 68.87, 63.25, 70.78, 66.0, 74.59, 77.91, 78.83, 76.99, 65.9, 73.38, 68.21, 70.04, 75.48, 74.77, 79.72, 84.21, 81.66, 76.23, 70.84, 76.02, 87.41, 87.63, 95.73, 99.79, 100.31, 101.45, 116.38, 117.96, 119.63, 121.72, 126.78, 133.26, 137.95, 147.62, 148.73], 
'S&P Global Inc. Common Stock': [117.48, 120.71, 116.22, 113.49, 102.88, 114.97, 123.86, 125.47, 128.78, 137.05, 140.52, 147.83, 148.55, 150.86, 151.02, 159.71, 163.9, 175.23, 185.58, 185.36, 182.97, 191.6, 198.3, 194.94, 201.37, 190.5, 177.76, 178.28, 166.16, 187.38, 195.91, 206.44, 216.36, 209.71, 223.94, 240.81, 255.8, 241.38, 254.2, 260.76, 269.62, 290.04, 262.57, 242.53, 289.86, 321.67, 326.79, 347.39, 363.43, 358.32, 320.69, 349.56, 327.3, 315.63, 327.93, 352.15, 389.6, 378.7, 410.45, 414.42]}
solver(adj_close)
