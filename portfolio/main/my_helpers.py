from datetime import date
import numpy as np
from numpy.linalg import solve
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
# from pypfopt import black_litterman
from pypfopt.black_litterman import BlackLittermanModel
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
        ave_return+= np.average(ret[key])*weights[key]
        ave_return = round(ave_return, 2)
    portfolio_vol = get_portfolio_vol(ret, weights)
    stats = {'ave_return': ave_return, 'portfolio_vol': portfolio_vol}
    results = {'weights': weights, 'stats': stats}
    return results


def get_cov_matrix(returns_dict):
    ret_list = []
    for key in returns_dict:
        ret_list.append(returns_dict[key])
    # print(np.cov(ret_list, ddof=1))
    return np.cov(ret_list, ddof=1)

def get_portfolio_vol(returns_dict, weights_dict):
    weights = []
    for key in weights_dict:
        weights.append(weights_dict[key])
    cov_matrix = get_cov_matrix(returns_dict)
    portfolio_var = np.matmul(weights, np.matmul(cov_matrix, weights))
    # print(np.sqrt(portfolio_var))
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
    return_series = pd.Series(exp_ret)
    cov = get_cov_matrix(ret)
    df = pd.DataFrame.from_records(cov)
    df.columns=[key for key in exp_ret]
    df.index = [key for key in exp_ret]
    ef = EfficientFrontier(return_series, cov, weight_bounds=(-1,1))
    weights_msr = {}
    for item in ef.max_sharpe().items():
        weights_msr[item[0]] = round(item[1]*100, 2)
    stats_msr = []
    for i in range(len(ef.portfolio_performance(verbose=False))):
        stats_msr.append(round(ef.portfolio_performance(verbose=False)[i]*100, 2))
    es = EfficientFrontier(return_series, cov, weight_bounds=(-1,1))
    weights_min = {}
    stats_min = []
    for item in es.min_volatility().items():
        weights_min[item[0]] = round(item[1]*100, 2)
    for i in range(len(es.portfolio_performance(verbose=False))):
        stats_min.append(round(es.portfolio_performance(verbose=False)[i]*100, 2))
    # print(weights_min)
    results = {
        'weights_msr': weights_msr,
        'stats_msr': stats_msr,
        'weights_min': weights_min,
        'stats_min': stats_min
    }
    return results

viewdict = {"Tesla Inc. Common Stock": 0.20, "Xenetic Biosciences Inc. Common Stock": 0.30, 
                "Agilent Technologies Inc. Common Stock": 0, "Apple Inc. Common Stock": 0.2}
def bl_portfolio(dict_adj, *views):
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
    return_series = pd.Series(exp_ret)
    cov = get_cov_matrix(ret)
    df = pd.DataFrame.from_records(cov)
    df.columns=[key for key in exp_ret]
    df.index = [key for key in exp_ret]
    # viewdict = {"Tesla Inc. Common Stock": 0.20, "Xenetic Biosciences Inc. Common Stock": -0.30, 
    #             "Agilent Technologies Inc. Common Stock": 0, "Apple Inc. Common Stock": 0.2}
    # prior = [exp_ret[key] for key in exp_ret]
    if len(views) == 0:
        return solver(dict_adj)
    for key in views[0]:
        views[0][key]/=100
    bl = BlackLittermanModel(df, absolute_views=views[0])
    returns = bl.bl_returns()
    ef = EfficientFrontier(returns, cov, weight_bounds=(-1,1))
    es = EfficientFrontier(returns, cov, weight_bounds=(-1,1))
    weights_msr = {}
    for item in ef.max_sharpe().items():
        weights_msr[item[0]] = round(item[1]*100, 2)
    stats_msr = []
    for i in range(len(ef.portfolio_performance(verbose=False))):
        stats_msr.append(round(ef.portfolio_performance(verbose=False)[i]*100, 2))
    weights_min = {}
    stats_min = []
    for item in es.min_volatility().items():
        weights_min[item[0]] = round(item[1]*100, 2)
    for i in range(len(es.portfolio_performance(verbose=False))):
        stats_min.append(round(es.portfolio_performance(verbose=False)[i]*100, 2))
    results = {
        'weights_msr': weights_msr,
        'stats_msr': stats_msr,
        'weights_min': weights_min,
        'stats_min': stats_min
    }
    return results

# data = {'Tesla Inc. Common Stock': [42.4, 40.81, 39.55, 37.88, 42.74, 50.39, 50.0, 55.66, 62.81, 68.2, 72.32, 64.69, 71.18, 68.22, 66.31, 61.77, 62.27, 70.86, 68.61, 53.23, 58.78, 56.95, 68.59, 59.63, 60.33, 52.95, 67.46, 70.1, 66.56, 61.4, 63.98, 55.97, 47.74, 37.03, 44.69, 48.32, 45.12, 48.17, 62.98, 65.99, 83.67, 130.11, 133.6, 104.8, 156.38, 167.0, 215.96, 286.15, 498.32, 429.01, 388.04, 567.6, 705.67, 793.53, 675.5, 667.93, 709.44, 625.22, 679.7, 655.29],
# 'Xenetic Biosciences Inc. Common Stock': [60.6, 54.0, 55.2, 44.64, 51.6, 59.16, 50.064, 54.6, 56.256, 37.44, 33.12, 37.68, 29.04, 24.24, 25.68, 25.44, 23.028, 25.08, 23.4, 25.8, 21.48, 18.72, 48.96, 35.4, 35.64, 33.96, 29.4, 39.6, 19.68, 22.32, 27.6, 23.28, 17.28, 8.16, 11.25, 2.41, 1.66, 1.197, 1.21, 1.23, 1.44, 1.42, 0.988, 0.741, 0.925, 1.004, 1.02, 1.17, 1.04, 0.905, 0.864, 1.14, 2.04, 2.37, 2.39, 2.18, 1.96, 1.91, 2.04, 1.91],
# 'Agilent Technologies Inc. Common Stock': [45.0, 45.11, 41.84, 42.23, 43.75, 47.16, 49.41, 50.92, 53.15, 58.26, 57.26, 57.85, 62.62, 62.12, 65.83, 67.14, 64.94, 71.36, 66.65, 65.01, 63.88, 60.31, 60.23, 64.32, 65.94, 68.87, 63.25, 70.78, 66.0, 74.59, 77.91, 78.83, 76.99, 65.9, 73.38, 68.21, 70.04, 75.48, 74.77, 79.72, 84.21, 81.66, 76.23, 70.84, 76.02, 87.41, 87.63, 95.73, 99.79, 100.31, 101.45, 116.38, 117.96, 119.63, 121.72, 126.78, 133.26, 137.95, 147.62, 148.75],
# 'Apple Inc. Common Stock': [24.78, 26.55, 26.66, 25.95, 27.34, 28.64, 32.33, 34.05, 34.05, 36.21, 34.28, 35.4, 39.04, 36.83, 40.39, 41.06, 40.58, 40.15, 42.72, 40.4, 39.79, 45.0, 44.74, 46.0, 55.02, 54.76, 53.09, 43.32, 38.4, 40.51, 42.15, 46.43, 49.06, 42.8, 48.57, 52.28, 51.22, 55.17, 61.28, 65.83, 72.55, 76.47, 67.54, 62.98, 72.76, 78.74, 90.59, 105.55, 128.18, 115.24, 108.33, 118.47, 132.27, 131.54, 120.87, 121.94, 131.24, 124.4, 136.96, 145.4]}
# newviews = {"Tesla Inc. Common Stock": -.9, "Xenetic Biosciences Inc. Common Stock": -0.30, 
#                 "Agilent Technologies Inc. Common Stock": 0, "Apple Inc. Common Stock": 0.2}

# views = {'company_name 1': 'Agilent Technologies Inc. Common Stock', 'percentage 1': '10', 'company_name 2': 'Apple Inc. Common Stock', 'percentage 2': '10.5', 'company_name 3': 'C3.ai Inc. Class A Common Stock', 'percentage 3': '11.9', 'company_name 4': 'Herzfeld Caribbean Basin Fund Inc. (The) Common Stock', 'percentage 4': '10'}
# keys = list(views.keys())
# print(len(keys))
# a = {}
# for i in range(0,len(keys)-1, 2):
#     a[views[keys[i]]] = float(views[keys[i+1]])
# print(a)

