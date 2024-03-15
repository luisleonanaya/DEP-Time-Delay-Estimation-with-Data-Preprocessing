# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 01:46:32 2023

@author: luis
"""
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from skimage.restoration import (denoise_wavelet)


def waveletDenoise(ts1, ts2, trudelay, level=2):
    """
    Applies wavelet denoising to light curve data using the VisuShrink method, 
    significantly reducing noise while preserving the signal's key features. 
    The denoised data is then normalized and prepared for further analysis, 
    such as time-delay estimation.
    
    Parameters:
        ts1 (DataFrame): DataFrame containing the first light curve's data.
        ts2 (DataFrame): DataFrame for the second light curve.
        trudelay (int): Known time delay between the two light curves.
        level (int, optional): Decomposition level for the wavelet transform. Defaults to 2.
        
    Returns:
        dfWD_lcA (DataFrame): Denoised and normalized DataFrame for light curve A.
        dfWD_lcB (DataFrame): Denoised and normalized DataFrame for light curve B.
    """
    # Extract required columns
    dfA = ts1
    dfB = ts2
    time = dfA['time']

    # Ensure the time index is in one dimension for processing
    x = dfA['time'].to_numpy()
    x = np.reshape(x, (len(x), 1))

    # Apply the Wavelet denoise algorithm to both light curves
    # method='VisuShrink' applies universal thresholding
    y_denoise = denoise_wavelet(dfA['lc_A'], method='VisuShrink', mode='soft', wavelet_levels=level, wavelet='coif17', rescale_sigma='True')
    y1_denoise = denoise_wavelet(dfB['lc_B'], method='VisuShrink', mode='soft', wavelet_levels=level, wavelet='coif17', rescale_sigma='True')
    
    # Convert the denoised light curves to DataFrame columns
    dfWavDenoise_lcA = pd.DataFrame(y_denoise)
    dfWavDenoise_lcB = pd.DataFrame(y1_denoise)
       
    # Normalize the denoised time series
    scaler = MinMaxScaler(feature_range=(0.01, 1))
    dfWavDenoise_lcA = scaler.fit_transform(dfWavDenoise_lcA.values.reshape(-1, 1)).flatten()
    dfWavDenoise_lcB = scaler.fit_transform(dfWavDenoise_lcB.values.reshape(-1, 1)).flatten()

    # Calculate the error for the denoised and normalized light curves
    lcA_WavErr = dfWavDenoise_lcA * dfA['pctErr_A']
    lcB_WavErr = dfWavDenoise_lcB * dfB['pctErr_B']

    # Construct DataFrames with denoised data and recalculated errors
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
    
    return dfWD_lcA, dfWD_lcB


