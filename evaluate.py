# standard imports
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

def plot_baseline(x, y):
    '''
    Takes in: independent variable (x) and actual values for target (y)
    Returns: a plot of the baseline prediction
    '''
    plt.scatter(x, y)
    plt.axhline(y.mean(), ls = ':', color='black')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Baseline model');
    
def plot_model(x, y, yhat):
    '''
    Takes in: independent variable (x), actual values for target (y), predicted values for target (yhat)
    Returns: plot of data points and line of best fit produced by model
    '''
    plt.scatter(x, y)
    plt.plot(x, yhat, color='black')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Linear Model');
    
def plot_baseline_and_model(x, y, yhat):
    '''
    Takes in: independent variable (x), actual values for target (y), predicted values for target (yhat)
    Returns: plot of baseline and line of best fit produced by model 
    '''
    plt.figure(figsize = (11,5))

    plt.subplot(121)
    plt.scatter(x, y)
    plt.axhline(y.mean(), ls = ':', color='black')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Baseline Model')
    
    plt.subplot(122)
    plt.scatter(x, y)
    plt.plot(x, yhat, color='black')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Linear Model');

def plot_residuals(x, y, yhat):
    '''
    Takes in: independent variable (x), actual values for target (y), and predicted values for target (yhat)
    Returns: a plot of baseline residuals and a plot of model residuals
    '''
    plt.figure(figsize = (11,5))

    plt.subplot(121)
    plt.scatter(x, y - y.mean())
    plt.axhline(y = 0, ls = ':', color='black')
    plt.xlabel('x')
    plt.ylabel('Residual')
    plt.title('Baseline Residuals')
    
    plt.subplot(122)
    plt.scatter(x, y - yhat)
    plt.axhline(y = 0, ls = ':', color='black')
    plt.xlabel('x')
    plt.ylabel('Residual')
    plt.title('Model residuals');
    
def regression_errors_all(y, yhat):
    '''
    Takes in: actual values for target (y) and predicted values for target (yhat)
    Returns: SSE, MSE, RMSE, ESS, TSS, R2
    '''
    SSE = ((y - yhat)**2).sum()
    MSE = SSE / len(y)
    RMSE = MSE ** (1/2)
    ESS = ((yhat - y.mean())**2).sum()
    TSS = SSE + ESS
    R2 = ESS / TSS
    return SSE, MSE, RMSE, ESS, TSS, R2

def regression_errors(y, yhat):
    '''
    Takes in: actual values for target (y) and predicted values for target (yhat)
    Returns: RMSE, R2
    '''
    SSE = ((y - yhat)**2).sum()
    MSE = SSE / len(y)
    RMSE = MSE ** (1/2)
    ESS = ((yhat - y.mean())**2).sum()
    TSS = SSE + ESS
    R2 = ESS / TSS
    return RMSE, R2

def baseline_mean_errors(y):
    '''
    Takes in: actual values for target (y)
    Returns: baseline SSE, MSE, RMSE
    '''
    SSE = ((y - y.mean())**2).sum()
    MSE = SSE / len(y)
    RMSE = MSE ** (1/2)
    return SSE, MSE, RMSE

def better_than_baseline(y, yhat):
    '''
    Takes in: actual values for target (y) and predicted values for target (yhat)
    Returns: True if model outperforms baseline, false if not
    '''
    SSE = ((y - yhat)**2).sum()
    SSE_baseline = ((y - y.mean())**2).sum()
    if SSE < SSE_baseline:
        return True
    else:
        return False