# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 22:41:50 2023

@author: luis
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler


def raw_data(ts1, ts2, trudelay):
# Extraer las columnas requeridas
    #dfA = pd.read_csv(ts1)
    #dfB = pd.read_csv(ts2) 
    dfA = ts1
    dfB = ts2
    
    time = dfA['time']
    lc_A = dfA['lc_A']
    lc_B = dfB['lc_B']
    
    # Realizar la estandarización de las series de tiempo
    scaler = MinMaxScaler(feature_range=(0.1, 1))
    lc_A = scaler.fit_transform(lc_A.values.reshape(-1, 1)).flatten()
    lc_B = scaler.fit_transform(lc_B.values.reshape(-1, 1)).flatten()

    err_A = lc_A * dfA['pctErr_A']
    err_B = lc_B * dfB['pctErr_B']


    lightCurve_A = {
    'time': time,
    'lc_A': lc_A,
    'err_A': err_A,
    }
    
    lightCurve_B = {
    'time': time,
    'lc_B': lc_B,
    'err_B': err_B,
    }
        
    df_lcA = pd.DataFrame(lightCurve_A)
    df_lcB = pd.DataFrame(lightCurve_B)
    
    return df_lcA, df_lcB