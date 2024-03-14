# -*- coding: utf-8 -*-
"""
Created on Thu Jun 15 04:15:22 2023

@author: luis
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from sklearn.preprocessing import MinMaxScaler


def cf_filter(ts1, ts2, trudelay):
# Extraer las columnas requeridas
    #dfA = pd.read_csv(ts1)
    #dfB = pd.read_csv(ts2) 
    
    dfA = ts1
    dfB = ts2 
    
    time = dfA['time']
    #Convert both time series to numpy
    df_lcA_numpy = dfA['lc_A'].to_numpy()
    df_lcA_numpy.flatten()
    df_lcB_numpy = dfB['lc_B'].to_numpy()
    df_lcB_numpy.flatten()
    #Apply the CF filter algorithm to both light curves
    cycleA, trendA = sm.tsa.filters.cffilter(df_lcA_numpy, 2, 8, drift=False)
    cycleB, trendB = sm.tsa.filters.cffilter(df_lcB_numpy, 2, 8, drift=False)
    
    #Converting the CF cycle and trend numpy array (light curve A) to a dataframe column 
    dfCycle_lcA = pd.DataFrame(cycleA)
    dfTrend_lcA = pd.DataFrame(trendA)
    #Converting the CF cycle and trend numpy array (light curve B) to a dataframe column
    dfCycle_lcB = pd.DataFrame(cycleB)
    dfTrend_lcB = pd.DataFrame(trendB)

    #declaro el minmax estandarizacion
    scaler = MinMaxScaler(feature_range=(0.01, 1))
    # Realizar la estandarización de la curva de luz A
    dfCycle_lcA = scaler.fit_transform(dfCycle_lcA.values.reshape(-1, 1)).flatten()
    dfTrend_lcA = scaler.fit_transform(dfTrend_lcA.values.reshape(-1, 1)).flatten()
    # Realizar la estandarización de la curva de luz B
    dfCycle_lcB = scaler.fit_transform(dfCycle_lcB.values.reshape(-1, 1)).flatten()
    dfTrend_lcB = scaler.fit_transform(dfTrend_lcB.values.reshape(-1, 1)).flatten()
    # calculating the error for light curve A
    dfCycle_lcA_Err = abs(dfCycle_lcA * dfA['pctErr_A'])
    dfTrend_lcA_Err = abs(dfTrend_lcA * dfA['pctErr_A'])
    # calculating the error for light curve B
    dfCycle_lcB_Err = abs(dfCycle_lcB * dfB['pctErr_B'])
    dfTrend_lcB_Err = abs(dfTrend_lcB * dfB['pctErr_B'])
    
    lightCurve_A_cycle = {
    'time': time,
    'dfCycle_lcA': dfCycle_lcA,
    'dfCycle_lcA_Err': dfCycle_lcA_Err,
    }
    
    lightCurve_B_cycle = {
    'time': time,
    'dfCycle_lcB': dfCycle_lcB,
    'dfCycle_lcB_Err': dfCycle_lcB_Err,
    }
    
    lightCurve_A_trend = {
    'time': time,
    'dfTrend_lcA': dfTrend_lcA,
    'dfTrend_lcA_Err': dfTrend_lcA_Err,
    }
    
    lightCurve_B_trend = {
    'time': time,
    'dfTrend_lcB': dfTrend_lcB,
    'dfTrend_lcB_Err': dfTrend_lcB_Err,
    }
        
    df_CFcycle_lcA = pd.DataFrame(lightCurve_A_cycle)
    df_CFcycle_lcB = pd.DataFrame(lightCurve_B_cycle)
    df_CFtrend_lcA = pd.DataFrame(lightCurve_A_trend)
    df_CFtrend_lcB = pd.DataFrame(lightCurve_B_trend)
    
    # Save dfCycle A and B to CSV
    #df_CFcycle_lcA.to_csv('dfCycle_ts1.csv', index=False)
    #df_CFcycle_lcB.to_csv('dfCycle_ts2.csv', index=False)
    # Save dfTrend A and B to CSV
    #df_CFtrend_lcA.to_csv('dfTrend_ts1.csv', index=False)
    #df_CFtrend_lcB.to_csv('dfTrend_ts2.csv', index=False)
    
    return df_CFcycle_lcA, df_CFcycle_lcB, df_CFtrend_lcA, df_CFtrend_lcB
    
    
    
    
