from datetime import date
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
    for i in range(len(ef.portfolio_performance(verbose=True))):
        stats_msr.append(round(ef.portfolio_performance(verbose=True)[i]*100, 2))
    es = EfficientFrontier(return_series, cov, weight_bounds=(-1,1))
    weights_min = {}
    stats_min = []
    for item in es.min_volatility().items():
        weights_min[item[0]] = round(item[1]*100, 2)
    for i in range(len(es.portfolio_performance(verbose=True))):
        stats_min.append(round(es.portfolio_performance(verbose=True)[i]*100, 2))
    # print(weights_min)
    results = {
        'weights_msr': weights_msr,
        'stats_msr': stats_msr,
        'weights_min': weights_min,
        'stats_min': stats_min
    }
    return results


