import numpy as np

def risk_parity(dict_adj):
    stdev = {}
    total_std = 0
    for key in dict_adj:
        stdev[key] = np.std(dict_adj[key], ddof=1)
        total_std+=1/stdev[key]
    weights = {}
    for key in dict_adj:
        weights[key]=round(100*(1/stdev[key])/total_std, 2)
    return weights
        
