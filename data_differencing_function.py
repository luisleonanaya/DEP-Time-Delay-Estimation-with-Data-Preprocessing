# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 04:20:11 2023

@author: luis
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
"""
df = pd.read_csv('tdc1_rung3_double_pair434.txt', skiprows=[0,1, 2, 3, 4, 5 ], header=None, delim_whitespace=True, names=('time','lc_A','err_A','lc_B','err_B'))
#percentage error for both light curves

# Option 1: Split based on columns
df1 = df[['time', 'lc_A', 'err_A']].copy()
df2 = df[['time', 'lc_B', 'err_B']].copy()

df1.loc[:, 'pctErr_A'] = df1['err_A'] / df1['lc_A']
df2.loc[:, 'pctErr_B'] = df2['err_B'] / df2['lc_B']
#display first five lines of the DataFrame
print(df1)

# Save df1 to CSV
df1.to_csv('df1.csv', index=False)

# Save df2 to CSV
df2.to_csv('df2.csv', index=False)
"""


def data_differencing(ts1, ts2, trudelay):
# Extraer las columnas requeridas
    dfA = ts1
    dfB = ts2
    
    time_diff = dfA['time']
    time_diff = time_diff.tail(-1)

    differenced_mag_A = dfA['lc_A'].diff()
    differenced_mag_B = dfB['lc_B'].diff()

     # Realizar la estandarización de las series de tiempo
    scaler = MinMaxScaler(feature_range=(0.1, 1))
    differenced_mag_A = scaler.fit_transform(differenced_mag_A.values.reshape(-1, 1)).flatten()
    differenced_mag_B = scaler.fit_transform(differenced_mag_B.values.reshape(-1, 1)).flatten()

    diff_magerr_A =  differenced_mag_A * dfA['pctErr_A']
    diff_magerr_B = differenced_mag_B * dfB['pctErr_B']

    differenced_mag_A = pd.Series(differenced_mag_A).tail(-1)
    diff_magerr_A = pd.Series(diff_magerr_A).tail(-1)
    differenced_mag_B = pd.Series(differenced_mag_B).tail(-1)
    diff_magerr_B = pd.Series(diff_magerr_B).tail(-1)

    lightCurve_A = {
    'time_diff': time_diff,
    'differenced_mag_A': differenced_mag_A,
    'diff_magerr_A': diff_magerr_A,
    }
    
    lightCurve_B = {
    'time_diff': time_diff,
    'differenced_mag_B': differenced_mag_B,
    'diff_magerr_B': diff_magerr_B
    }
        
    df_lcA = pd.DataFrame(lightCurve_A)
    df_lcB = pd.DataFrame(lightCurve_B)
    
    return df_lcA, df_lcB
    """
    # Save df1 to CSV
    df_lcA.to_csv('dfDtaDiffts1.csv', index=False)

    # Save df2 to CSV
    df_lcB.to_csv('dfDtaDiffts2.csv', index=False)
    
    fig1, ax1 = plt.subplots()
    fig2, ax2 = plt.subplots()
    # Graficar las series de tiempo con líneas que conectan los puntos y color personalizado
    ax1.errorbar(time_diff, differenced_mag_A, yerr=diff_magerr_A, fmt='o-', markersize=2, label='mag_A', color='blue', linewidth=0.4)
    ax1.plot(time_diff, differenced_mag_A, linewidth=0.3, color='black')
    ax1.set_xlabel('time')
    ax1.set_ylabel('Magnitud')
    ax1.set_title(' mag_A')

    ax2.errorbar(time_diff, differenced_mag_B, yerr=diff_magerr_B, fmt='o-', markersize=2, label='mag_B', color='green', linewidth=0.4)
    ax2.plot(time_diff, differenced_mag_B, linewidth=0.3, color='black')
    ax2.set_xlabel('time')
    ax2.set_ylabel('Magnitud')
    ax2.set_title(' mag_B')
    """