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
    """
    Calculates the simple net return (SNR) for light curve data, a method commonly used 
    to quantify relative changes over time. This function applies SNR calculation to light 
    curve magnitudes, followed by MinMax scaling to normalize the data. The process prepares 
    the dataset for in-depth analysis by enhancing the visibility of variations and trends.
    
    Parameters:
        ts1 (DataFrame): Contains the first light curve's data, including time ('time'), 
        magnitude ('lc_A'), and percentage error ('pctErr_A').
        ts2 (DataFrame): Similar to ts1, but for the second light curve ('lc_B' and 'pctErr_B').
        trudelay (int): Known time delay between the light curves, reserved for future use.
        
    Returns:
        df_snr_lcA (DataFrame): DataFrame for light curve A, with SNR magnitudes, 
        corresponding time points, and recalculated errors.
        df_snr_lcB (DataFrame): Similar to df_snr_lcA, for light curve B.
    """
    
    # Extracting the required columns from input DataFrames
    dfA = ts1
    dfB = ts2
    
    # Preparing the time series for SNR calculation (excluding the first value due to differencing)
    time_snr = dfA['time'].tail(-1)  # Remove the first time point as it has no previous point to compare

    # Calculating Simple Net Return (SNR) by computing the percentage change between consecutive magnitudes
    snr_mag_A = dfA['lc_A'].pct_change()  # SNR for light curve A
    snr_mag_B = dfB['lc_B'].pct_change()  # SNR for light curve B

    # Standardizing the time series using MinMaxScaler to ensure they are on a common scale
    scaler = MinMaxScaler(feature_range=(0.01, 1))
    snr_mag_A = scaler.fit_transform(snr_mag_A.values.reshape(-1, 1)).flatten()  # Flatten to convert from 2D back to 1D
    snr_mag_B = scaler.fit_transform(snr_mag_B.values.reshape(-1, 1)).flatten()  # Flatten to convert from 2D back to 1D

    # Calculating the error for the SNR values based on the original percentage errors
    snr_magerr_A = snr_mag_A * dfA['pctErr_A']  # SNR errors for light curve A
    snr_magerr_B = snr_mag_B * dfB['pctErr_B']  # SNR errors for light curve B

    # Preparing the final DataFrames with SNR values and corresponding errors (excluding the first value due to differencing)
    snr_mag_A = pd.Series(snr_mag_A).tail(-1)  # Excluding the first value which is NaN due to pct_change()
    snr_magerr_A = pd.Series(snr_magerr_A).tail(-1)  # Matching error series length to SNR series
    snr_mag_B = pd.Series(snr_mag_B).tail(-1)  # Excluding the first value which is NaN due to pct_change()
    snr_magerr_B = pd.Series(snr_magerr_B).tail(-1)  # Matching error series length to SNR series

    # Constructing the output DataFrames for both light curves
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
    
    df_snr_lcA = pd.DataFrame(lightCurve_A)  # DataFrame for light curve A with SNR and errors
    df_snr_lcB = pd.DataFrame(lightCurve_B)  # DataFrame for light curve B with SNR and errors
    
    return df_snr_lcA, df_snr_lcB

