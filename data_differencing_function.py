# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 04:20:11 2023

@author: luis
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler


def data_differencing(ts1, ts2, trudelay):
    """
    Applies differencing to light curve data to highlight changes between consecutive measurements, 
    followed by MinMax scaling for normalization. This preprocessing step is crucial for time series analysis, 
    making patterns more discernible and reducing noise.
    
    Parameters:
        ts1 (DataFrame): DataFrame containing the first light curve's data, with 'time', 'lc_A', and 'pctErr_A'.
        ts2 (DataFrame): DataFrame for the second light curve, similar to ts1, but for 'lc_B' and 'pctErr_B'.
        trudelay (int): Known time delay between the light curves, reserved for future use.
        
    Returns:
        df_lcA (DataFrame): DataFrame for light curve A after differencing, with differenced magnitudes, time points, 
        and recalculated errors.
        df_lcB (DataFrame): Similar to df_lcA, for light curve B.
    """
    # Extract the required columns from the input DataFrames
    dfA = ts1
    dfB = ts2
    
    # Prepare the time series by removing the first value, as differencing reduces the series length by one
    time_diff = dfA['time'].tail(-1)  # Adjust the time array to match the length of the differenced data

    # Perform differencing on the light curve magnitudes to highlight changes between consecutive measurements
    differenced_mag_A = dfA['lc_A'].diff()  # Differencing for light curve A
    differenced_mag_B = dfB['lc_B'].diff()  # Differencing for light curve B

    # Normalize the differenced series using MinMaxScaler to bring them to a common scale
    scaler = MinMaxScaler(feature_range=(0.1, 1))
    differenced_mag_A = scaler.fit_transform(differenced_mag_A.values.reshape(-1, 1)).flatten()  # Flatten the array post-scaling
    differenced_mag_B = scaler.fit_transform(differenced_mag_B.values.reshape(-1, 1)).flatten()  # Flatten the array post-scaling

    # Calculate the errors for the differenced values based on original percentage errors
    diff_magerr_A = differenced_mag_A * dfA['pctErr_A']  # Error calculation for differenced light curve A
    diff_magerr_B = differenced_mag_B * dfB['pctErr_B']  # Error calculation for differenced light curve B

    # Removing the first NaN value resulted from the differencing operation
    differenced_mag_A = pd.Series(differenced_mag_A).tail(-1)  # Remove NaN value for A
    diff_magerr_A = pd.Series(diff_magerr_A).tail(-1)  # Adjust error series length for A
    differenced_mag_B = pd.Series(differenced_mag_B).tail(-1)  # Remove NaN value for B
    diff_magerr_B = pd.Series(diff_magerr_B).tail(-1)  # Adjust error series length for B

    # Constructing the output DataFrames with differenced and normalized magnitudes and corresponding errors
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
        
    df_lcA = pd.DataFrame(lightCurve_A)  # DataFrame for differenced and normalized light curve A
    df_lcB = pd.DataFrame(lightCurve_B)  # DataFrame for differenced and normalized light curve B
    
    return df_lcA, df_lcB

