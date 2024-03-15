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
    """
    Standardizes light curve magnitudes to a common scale and calculates associated errors. 
    This function prepares light curve data from gravitationally lensed quasars for further analysis 
    by applying MinMax scaling, making the dataset ready for time-delay estimation and other analytical processes.
    
    Parameters:
        ts1 (DataFrame): The first light curve data as a pandas DataFrame. It must contain columns 
        for time ('time'), light curve magnitude ('lc_A'), and percentage error ('pctErr_A').
        
        ts2 (DataFrame): The second light curve data as a pandas DataFrame, with similar columns 
        for the second light curve ('time', 'lc_B', and 'pctErr_B').
        
        trudelay (int): The true delay between the light curves. Currently, this parameter is included 
        for future enhancements and does not affect the function's processing.
        
    Returns:
        df_lcA (DataFrame): A pandas DataFrame containing the standardized light curve A ('lc_A'), 
        the time ('time'), and the calculated error ('err_A').
        
        df_lcB (DataFrame): Similar to df_lcA, but for light curve B ('lc_B'), including standardized 
        magnitudes, time, and errors.
        
    The function ensures that light curve data is processed on a consistent scale, facilitating accurate 
    comparison and analysis. By adjusting errors according to the standardized magnitudes, it maintains 
    data integrity for subsequent analytical steps.
    """
    # Extract the required columns from the input DataFrames
    dfA = ts1
    dfB = ts2
    
    # Copy the 'time' column from dfA as it will be used in both output DataFrames
    time = dfA['time']

    # Extracting light curve magnitudes for both A and B
    lc_A = dfA['lc_A']
    lc_B = dfB['lc_B']
    
    # Applying MinMax scaling to the light curve magnitudes to standardize them to a common scale
    scaler = MinMaxScaler(feature_range=(0.1, 1))  # Define the scaler with the specified range
    lc_A = scaler.fit_transform(lc_A.values.reshape(-1, 1)).flatten()  # Scale and flatten light curve A magnitudes
    lc_B = scaler.fit_transform(lc_B.values.reshape(-1, 1)).flatten()  # Scale and flatten light curve B magnitudes

    # Calculating the errors for the standardized light curves based on original percentage errors
    err_A = lc_A * dfA['pctErr_A']  # Error calculation for light curve A
    err_B = lc_B * dfB['pctErr_B']  # Error calculation for light curve B

    # Constructing the output DataFrames for both light curves including time, standardized magnitudes, and calculated errors
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
        
    df_lcA = pd.DataFrame(lightCurve_A)  # DataFrame for light curve A
    df_lcB = pd.DataFrame(lightCurve_B)  # DataFrame for light curve B
    
    return df_lcA, df_lcB
