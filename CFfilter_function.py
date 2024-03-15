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
    """
    Applies the Christiano-Fitzgerald (CF) filter to preprocess light curves, extracting cycle and trend components.
    This method is particularly useful for analyzing time series data, helping to identify underlying patterns or trends
    by separating the original series into cyclical and trend components.

    Parameters:
        ts1 (DataFrame): DataFrame containing the light curve data for object A, including time and magnitude.
        ts2 (DataFrame): DataFrame containing the light curve data for object B, structured like ts1.
        trudelay (int): The true delay between the light curves, intended for future use in enhancing filter application.

    Returns:
        df_CFcycle_lcA, df_CFcycle_lcB: DataFrames containing the cyclical components of each light curve.
        df_CFtrend_lcA, df_CFtrend_lcB: DataFrames containing the trend components of each light curve.
    """
    
    # Extract the required data from input DataFrames
    dfA = ts1
    dfB = ts2 
    time = dfA['time']  # Time column, assuming it's identical for both light curves
    
    # Convert light curve magnitudes to numpy arrays for processing
    df_lcA_numpy = dfA['lc_A'].to_numpy()
    df_lcB_numpy = dfB['lc_B'].to_numpy()
    
    # Apply the CF filter to both light curves to decompose into cycle and trend components
    cycleA, trendA = sm.tsa.filters.cffilter(df_lcA_numpy, 2, 8, drift=False)
    cycleB, trendB = sm.tsa.filters.cffilter(df_lcB_numpy, 2, 8, drift=False)
    
    # Convert the cycle and trend components back into pandas DataFrames for further processing
    dfCycle_lcA = pd.DataFrame(cycleA, columns=['Cycle'])
    dfTrend_lcA = pd.DataFrame(trendA, columns=['Trend'])
    dfCycle_lcB = pd.DataFrame(cycleB, columns=['Cycle'])
    dfTrend_lcB = pd.DataFrame(trendB, columns=['Trend'])
    
    # Initialize MinMaxScaler to standardize the components to a specific range
    scaler = MinMaxScaler(feature_range=(0.01, 1))
    
    # Standardize the cycle and trend components of both light curves
    dfCycle_lcA = scaler.fit_transform(dfCycle_lcA).flatten()
    dfTrend_lcA = scaler.fit_transform(dfTrend_lcA).flatten()
    dfCycle_lcB = scaler.fit_transform(dfCycle_lcB).flatten()
    dfTrend_lcB = scaler.fit_transform(dfTrend_lcB).flatten()
    
    # Calculate the error for the standardized cycle and trend components based on original percentage errors
    dfCycle_lcA_Err = abs(dfCycle_lcA * dfA['pctErr_A'])
    dfTrend_lcA_Err = abs(dfTrend_lcA * dfA['pctErr_A'])
    dfCycle_lcB_Err = abs(dfCycle_lcB * dfB['pctErr_B'])
    dfTrend_lcB_Err = abs(dfTrend_lcB * dfB['pctErr_B'])
    
    # Construct DataFrames to hold the cycle and trend components along with their errors
    lightCurve_A_cycle = {
        'time': time,
        'Cycle': dfCycle_lcA,
        'Error': dfCycle_lcA_Err,
    }
    lightCurve_B_cycle = {
        'time': time,
        'Cycle': dfCycle_lcB,
        'Error': dfCycle_lcB_Err,
    }
    lightCurve_A_trend = {
        'time': time,
        'Trend': dfTrend_lcA,
        'Error': dfTrend_lcA_Err,
    }
    lightCurve_B_trend = {
        'time': time,
        'Trend': dfTrend_lcB,
        'Error': dfTrend_lcB_Err,
    }
    
    # Create final output DataFrames for each component
    df_CFcycle_lcA = pd.DataFrame(lightCurve_A_cycle)
    df_CFcycle_lcB = pd.DataFrame(lightCurve_B_cycle)
    df_CFtrend_lcA = pd.DataFrame(lightCurve_A_trend)
    df_CFtrend_lcB = pd.DataFrame(lightCurve_B_trend)
    
    return df_CFcycle_lcA, df_CFcycle_lcB, df_CFtrend_lcA, df_CFtrend_lcB

    
    
    
    
