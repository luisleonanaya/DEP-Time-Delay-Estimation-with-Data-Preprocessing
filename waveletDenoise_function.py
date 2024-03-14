# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 01:46:32 2023

@author: luis
"""
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from skimage.restoration import (denoise_wavelet)


def waveletDenoise(ts1, ts2, trudelay, level = 2):
# Extraer las columnas requeridas
    dfA = ts1
    dfB = ts2
    level = level
    time = dfA['time']
    
    x = dfA['time'].to_numpy()
    x = np.reshape(x, (len(x), 1)) # ensure the index is in only one dimension

    #Apply the Wavelet denoise algorithm to both light curves
    y_denoise = denoise_wavelet(dfA['lc_A'], method='VisuShrink', mode='soft', wavelet_levels=level, wavelet='coif17',rescale_sigma='True')
    y1_denoise = denoise_wavelet(dfB['lc_B'], method='VisuShrink', mode='soft', wavelet_levels=level, wavelet='coif17',rescale_sigma='True')
    #Converting the denoised numpy array (light curve A) to a dataframe column and ocalculating the error
    dfWavDenoise_lcA = pd.DataFrame(y_denoise)
    dfWavDenoise_lcB = pd.DataFrame(y1_denoise)
       
    # Realizar la estandarización de las series de tiempo
    scaler = MinMaxScaler(feature_range=(0.01, 1))
    dfWavDenoise_lcA = scaler.fit_transform(dfWavDenoise_lcA.values.reshape(-1, 1)).flatten()
    dfWavDenoise_lcB = scaler.fit_transform(dfWavDenoise_lcB.values.reshape(-1, 1)).flatten()

    #Converting the denoised numpy array (light curve A and B) to a dataframe column and calculating the error
    lcA_WavErr = dfWavDenoise_lcA * dfA['pctErr_A']
    lcB_WavErr = dfWavDenoise_lcB * dfB['pctErr_B']
  
    """""
    The different methods for delay estimation have an input of two files 
    lcA[time,light curve A,lcA_Error] and lcB[time,light curve B,lcB_Error] 
    """""
    lightCurve_A = {
    'time': time,
    'dfWavDenoise_lcA': dfWavDenoise_lcA,
    'lcA_WavErr': lcA_WavErr,
    }
    
    lightCurve_B = {
    'time': time,
    'dfWavDenoise_lcB': dfWavDenoise_lcB,
    'lcB_WavErr': lcB_WavErr
    }
    
    dfWD_lcA = pd.DataFrame(lightCurve_A)
    dfWD_lcB = pd.DataFrame(lightCurve_B)
    
    # Save df1 to CSV
    #dfWD_lcA.to_csv('dfWDts1.csv', index=False)

    # Save df2 to CSV
    #dfWD_lcB.to_csv('dfWDts2.csv', index=False)
    
    return dfWD_lcA, dfWD_lcB
    
    
    #We save light curve A in cycle and trend in two separate files 
    #WDlcA_ts1 = df.iloc[0:,[0,7,8]].astype(float)
    #WDlcA_ts1.to_csv('WDlcA_ts1_r3_pair434.csv', index=False, header=False)
    #We save light curve B in cycle and trend in two separate files 
    #WDlcB_ts2 = df.iloc[0:,[0,9,10]].astype(float)
    #WDlcB_ts2.to_csv('WDlcB_ts2_r3_pair434.csv', index=False, header=False)
