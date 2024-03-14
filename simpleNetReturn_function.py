# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 04:48:14 2023

@author: luis
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler


def simple_net_return(ts1, ts2, trudelay):
# Extraer las columnas requeridas
    dfA = ts1
    dfB = ts2
    
    time_snr = dfA['time']
    time_snr = time_snr.tail(-1)
    #Simple Net return (SNR) calculation
    snr_mag_A = dfA['lc_A'].pct_change()
    snr_mag_B = dfB['lc_B'].pct_change()

    # Realizar la estandarización de las series de tiempo
    scaler = MinMaxScaler(feature_range=(0.01, 1))
    snr_mag_A = scaler.fit_transform(snr_mag_A.values.reshape(-1, 1)).flatten()
    snr_mag_B = scaler.fit_transform(snr_mag_B.values.reshape(-1, 1)).flatten()

    snr_magerr_A =  snr_mag_A * dfA['pctErr_A']
    snr_magerr_B = snr_mag_B * dfB['pctErr_B']

    snr_mag_A = pd.Series(snr_mag_A).tail(-1)
    snr_magerr_A = pd.Series(snr_magerr_A).tail(-1)
    snr_mag_B = pd.Series(snr_mag_B).tail(-1)
    snr_magerr_B = pd.Series(snr_magerr_B).tail(-1)

    lightCurve_A = {
    'time_snr': time_snr,
    'snr_mag_A': snr_mag_A,
    'snr_magerr_A': snr_magerr_A,
    }
    
    lightCurve_B = {
    'time_snr': time_snr,
    'snr_mag_B': snr_mag_B,
    'snr_magerr_B': snr_magerr_B
    }
        
    df_snr_lcA = pd.DataFrame(lightCurve_A)
    df_snr_lcB = pd.DataFrame(lightCurve_B)
    
    # Save df1 to CSV
    #df_snr_lcA.to_csv('dfSNRts1.csv', index=False)

    # Save df2 to CSV
    #df_snr_lcB.to_csv('dfSNRts2.csv', index=False)
    
    
    return df_snr_lcA, df_snr_lcB
