# -*- coding: utf-8 -*-
"""
Created on Sun Oct 15 18:00:19 2023

@author: luis
"""

from __future__ import print_function, division
#import sys
#sys.path.append('/time delay estimation tool/search_ranges')
import numpy as np
from search_ranges.delta_options_01_20 import delta_options_01_20
from search_ranges.delta_options_20_40 import delta_options_20_40
from search_ranges.delta_options_40_60 import delta_options_40_60
from search_ranges.delta_options_60_80 import delta_options_60_80
from search_ranges.delta_options_80_100 import delta_options_80_100
from search_ranges.delta_options_100_120 import delta_options_100_120
from search_ranges.delta_options_120_140 import delta_options_120_140
from search_ranges.delta_options_140_160 import delta_options_140_160
from search_ranges.delta_options_160_180 import delta_options_160_180
from search_ranges.delta_options_180_200 import delta_options_180_200
from search_ranges.delta_options_200_220 import delta_options_200_220
from search_ranges.delta_options_220_240 import delta_options_220_240
from search_ranges.delta_options_240_260 import delta_options_240_260
from search_ranges.delta_options_260_280 import delta_options_260_280
from search_ranges.delta_options_280_300 import delta_options_280_300
from search_ranges.delta_options_300_320 import delta_options_300_320
from search_ranges.delta_options_320_340 import delta_options_320_340
from search_ranges.delta_options_340_360 import delta_options_340_360
from search_ranges.delta_options_360_380 import delta_options_360_380
from search_ranges.delta_options_380_400 import delta_options_380_400
from search_ranges.delta_options_400_420 import delta_options_400_420
from search_ranges.delta_options_420_440 import delta_options_420_440
import pandas as pd
import numpy as np

# Define functions used within the main LNDCF calculation process

def adjust_time(lcA, lcB):
    """
    Synchronize the time columns of two light curve arrays by adjusting them
    to start from the same time point.

    Args:
    lcA (np.ndarray): Numpy array for the first light curve.
    lcB (np.ndarray): Numpy array for the second light curve.

    Returns:
    Tuple[np.ndarray, np.ndarray]: Adjusted light curve arrays.
    """
    # Find the minimum time value across both light curves
    adjust_time = min(np.min(lcA[:, 0]), np.min(lcB[:, 0]))

    # Adjust time columns so both start from the same point
    lcA[:, 0] -= adjust_time
    lcB[:, 0] -= adjust_time

    return lcA, lcB

def lightcurve_inspection(lightcurve):
    """
    Inspect the light curve array and adjust its format if necessary.
    This function ensures the light curve array has 3 columns.

    Args:
    lightcurve (np.ndarray): Light curve data.

    Returns:
    np.ndarray: Formatted light curve data.
    """
    # Ensure the light curve has the correct number of columns
    assert ((lightcurve.shape[1] == 2) or (lightcurve.shape[1] == 3)), "Light curve format mismatch"

    # If the light curve has 2 columns, add a third column with zeros
    if lightcurve.shape[1] == 2:
        lc_pack = np.zeros((lightcurve.shape[0], 3))
        lc_pack[:, 0:2] = lightcurve[:, 0:2]
        return lc_pack
    else:
        return lightcurve

# Main function to pre-process and prepare light curves
def preformat_lightcurves(df_lcA, df_lcB):
    """
    Prepare light curves for analysis by adjusting their time scales and normalizing them.

    Args:
    df_lcA (pd.DataFrame): DataFrame for the first light curve.
    df_lcB (pd.DataFrame): DataFrame for the second light curve.

    Returns:
    Tuple[np.ndarray, np.ndarray]: Prepared light curve arrays.
    """
    # Convert DataFrames to NumPy arrays
    lc_A = df_lcA.values
    lc_B = df_lcB.values

    # Inspect and adjust the format of light curves
    lc_A = lightcurve_inspection(lc_A)
    lc_B = lightcurve_inspection(lc_B)

    # Synchronize the time columns of the light curves
    lc_A, lc_B = adjust_time(lc_A, lc_B)

    # Subtract the mean from the data columns to normalize the light curves
    lc_A[:, 1] -= np.mean(lc_A[:, 1])
    lc_B[:, 1] -= np.mean(lc_B[:, 1])
    
    return lc_A, lc_B
    
    
def lndcf(lcA, lcB, t, dt):
    #locally normalized discrete cross-correlation function method
    lndcf = np.zeros(t.shape[0])
    lndcferr = np.zeros(t.shape[0])
    n = np.zeros(t.shape[0])

    dst = np.empty((lcA.shape[0], lcB.shape[0]))
    for i in range(lcA.shape[0]):
        for j in range(lcB.shape[0]):
            dst[i,j] = lcB[j,0] - lcA[i,0]

    for k in range(t.shape[0]):
        tlo = t[k] - dt/2.0
        thi = t[k] + dt/2.0
        ts1idx, ts2idx = np.where((dst < thi) & (dst > tlo))

        mts2 = np.mean(lcB[ts2idx,1])
        mts1 = np.mean(lcA[ts1idx,1])
        n[k] = ts1idx.shape[0]

        lndcf_low = np.sqrt((np.var(lcA[ts1idx,1]) - np.mean(lcA[ts1idx,2])**2) * (np.var(lcB[ts2idx,1]) - np.mean(lcB[ts2idx,2])**2))

        lndcf_upper = (lcB[ts2idx,1] - mts2) * (lcA[ts1idx,1] - mts1) /  lndcf_low
        
        if n[k] > 0:
            lndcf[k] = np.sum(lndcf_upper) / float(n[k])
        else:
            lndcf[k] = 0.0001  # Set dcf[k] to 0.0 when n[k] is 0
    
        if n[k] > 1:
            lndcferr[k] = np.sqrt(np.sum((lndcf_upper - lndcf[k])**2)) / float(n[k] - 1)
        else:
            lndcferr[k] = 0.0001  # Set dcferr[k] to 0.0001 when n[k] is 1

    return lndcf, lndcferr

tope = 1

trueDelay = 0
delta_min = 0
delta_max = 0

min_value = 0
max_value = 0
bandera_01_20 = None
bandera_20_40 = None
bandera_40_60 = None
bandera_60_80 = None
bandera_80_100 = None
bandera_100_120 = None
bandera_120_140 = None
bandera_140_160 = None
bandera_160_180 = None
bandera_180_200 = None
bandera_200_220 = None
bandera_220_240 = None
bandera_240_260 = None
bandera_260_280 = None
bandera_280_300 = None
bandera_300_320 = None
bandera_320_340 = None
bandera_340_360 = None
bandera_360_380 = None
bandera_380_400 = None
bandera_400_420 = None
bandera_420_440 = None

def find_lndcf_delay(fuenteLead, fuenteDelayed, trudelay, prep_technique):
    prep_technique = prep_technique
    dcf_Results = None
    list_lndcf = []
    min_value = None
    max_value = None
    i = 1.5 #iteration/bin 1/1.5, 2/2.0, 3/2.5, 4/3.0, 5/3.5, 6/4.0, 7/4.5, 8/5.0
    trueDelay = trudelay
    bandera_01_20 = 0
    bandera_20_40 = 0
    bandera_40_60 = 0
    bandera_60_80 = 0
    bandera_80_100 = 0
    bandera_100_120 = 0
    bandera_120_140 = 0
    bandera_140_160 = 0
    bandera_160_180 = 0
    bandera_180_200 = 0
    bandera_200_220 = 0
    bandera_220_240 = 0
    bandera_240_260 = 0
    bandera_260_280 = 0
    bandera_280_300 = 0
    bandera_300_320 = 0
    bandera_320_340 = 0
    bandera_340_360 = 0
    bandera_360_380 = 0
    bandera_380_400 = 0
    bandera_400_420 = 0
    bandera_420_440 = 0
    
    for p in range(1):
        if 0.1 <= trueDelay <= 20.00:
                 delta_min, delta_max,  bandera_01_20, tope, range_low, range_high = 1, 15, 1, 35, 0.50, 20.05
        elif 20.00 < trueDelay <= 40.00:
                 delta_min, delta_max, bandera_20_40, tope, range_low, range_high = 1, 35, 1, 47, 19.95, 40.05
        elif 40.00 < trueDelay <= 60.00:
                 delta_min, delta_max, bandera_40_60, tope, range_low, range_high = 5, 55, 1, 60, 39.95, 60.05
        elif 60.00 < trueDelay <= 80.00:
                 delta_min, delta_max, bandera_60_80, tope, range_low, range_high = 5, 75, 1, 34, 59.95, 80.05
        elif 80.00 < trueDelay <= 100.00:
              delta_min, delta_max, bandera_80_100, tope, range_low, range_high = 10, 110, 1, 42, 79.95, 100.05
        elif 100.00 < trueDelay <= 120.00:
            delta_min, delta_max, bandera_100_120, tope, range_low, range_high = 10, 120,  1, 32, 99.95, 120.05
        elif 120.00 < trueDelay <= 140.00:
            delta_min, delta_max, bandera_120_140, tope, range_low, range_high = 85, 135,  1, 29, 119.95, 140.05
        elif 140.00 < trueDelay <= 160.00:
            delta_min, delta_max, bandera_140_160, tope, range_low, range_high = 105, 155, 1, 29, 139.95, 160.05
        elif 160.00 < trueDelay <= 180.00:
            delta_min, delta_max, bandera_160_180, tope, range_low, range_high = 125, 175, 1, 29, 159.95, 180.05
        elif 180.00 < trueDelay <= 200.00:
            delta_min, delta_max, bandera_180_200, tope, range_low, range_high = 145, 195, 1, 29, 179.95, 200.05
        elif 200.00 < trueDelay <= 220.00:
            delta_min, delta_max, bandera_200_220, tope, range_low, range_high = 165, 215, 1, 29, 199.95, 220.05
        elif 220.00 < trueDelay <= 240.00:
            delta_min, delta_max, bandera_220_240, tope, range_low, range_high = 185, 235, 1, 29, 219.95, 240.05
        elif 240.00 < trueDelay <= 260.00:
            delta_min, delta_max, bandera_240_260, tope, range_low, range_high = 205, 255, 1, 29, 239.95, 260.05
        elif 260.00 < trueDelay <= 280.00:
            delta_min, delta_max, bandera_260_280, tope, range_low, range_high = 225, 275, 1, 29, 259.95, 280.05
        elif 280.00 < trueDelay <= 300.00:
            delta_min, delta_max, bandera_280_300, tope, range_low, range_high = 245, 295, 1, 29, 279.95, 300.05
        elif 300.00 < trueDelay <= 320.00:
            delta_min, delta_max, bandera_300_320, tope, range_low, range_high = 265, 315, 1, 29, 299.95, 320.05
        elif 320.00 < trueDelay <= 340.00:
            delta_min, delta_max, bandera_320_340, tope, range_low, range_high = 285, 335, 1, 29, 319.95, 340.05
        elif 340.00 < trueDelay <= 360.00:
            delta_min, delta_max, bandera_340_360, tope, range_low, range_high = 305, 355, 1, 29, 339.95, 360.05
        elif 360.00 < trueDelay <= 380.00:
            delta_min, delta_max, bandera_360_380, tope, range_low, range_high = 325, 375, 1, 29, 359.95, 380.05
        elif 380.00 < trueDelay <= 400.00:
            delta_min, delta_max, bandera_380_400, tope, range_low, range_high = 345, 395, 1, 29, 379.95, 400.05
        elif 400.00 < trueDelay <= 420.00:
            delta_min, delta_max, bandera_400_420, tope, range_low, range_high = 365, 415, 1, 29, 399.95, 420.05            
        elif 420.00 < trueDelay <= 440.00:
            delta_min, delta_max, bandera_420_440, tope, range_low, range_high = 385, 435, 1, 29, 419.95, 440.05  
            
        list_lndcf.append(["LNDCF_Max","LNDCFERR","EstimatedDelay", "bin", "delta min", "delta max", "True delay", "prep_technique","error"])
        for t in range(0,8):
            if t == 0:
                delta_min_initial = delta_min
                delta_max_initial = delta_max
            delta_min = delta_min_initial
            delta_max = delta_max_initial
            for k in range(tope):
                DT = i            
                N = int(np.around((delta_max - delta_min) / float(DT))) #N = np.around((upper1 - lower) / float(DT))
                T = np.linspace(delta_min + (DT / 2.0), delta_max - (DT / 2.0), N)
                TS1, TS2 = preformat_lightcurves(fuenteLead, fuenteDelayed)
                DCF, DCFERR = lndcf(TS1, TS2, T, DT)
                #if len(DCF) > 0:
                DCF = np.nan_to_num(DCF, nan=0.0)
                DCFERR = np.nan_to_num(DCFERR, nan=0.0)
                estimateDelay = float (T[np.argmax(DCF)])
                if range_low <= estimateDelay <= range_high:
                    list_lndcf.append([DCF.max(), DCFERR.max(), T[np.argmax(DCF)], i, delta_min, delta_max, trueDelay, prep_technique, abs(T[np.argmax(DCF)] - trueDelay)])
                ################################
                if bandera_01_20 == 1:
                    #print("entro al if bandera 01 20")
                    delta_tuple = (delta_min, delta_max)
                    if delta_tuple in delta_options_01_20:
                        delta_min, delta_max = delta_options_01_20[delta_tuple]
                elif bandera_20_40 == 1:
                    #print("entro al if bandera 20 40")
                    delta_tuple = (delta_min, delta_max)
                    if delta_tuple in delta_options_20_40:
                        delta_min, delta_max = delta_options_20_40[delta_tuple]                             
                elif bandera_40_60 == 1:
                    #print("entro al if bandera 40 60 ")
                    delta_tuple = (delta_min, delta_max)
                    if delta_tuple in delta_options_40_60:
                        delta_min, delta_max = delta_options_40_60[delta_tuple]
                elif bandera_60_80 == 1:
                    #print("entro al if bandera 60 80 ")
                    delta_tuple = (delta_min, delta_max)
                    if delta_tuple in delta_options_60_80:
                        delta_min, delta_max = delta_options_60_80[delta_tuple]
                elif bandera_80_100 == 1:
                     delta_tuple = (delta_min, delta_max)
                     if delta_tuple in delta_options_80_100:
                        delta_min, delta_max = delta_options_80_100[delta_tuple]
                elif bandera_100_120 == 1:
                     delta_tuple = (delta_min, delta_max)
                     if delta_tuple in delta_options_100_120:
                        delta_min, delta_max = delta_options_100_120[delta_tuple]
                elif bandera_120_140 == 1:
                     delta_tuple = (delta_min, delta_max)
                     if delta_tuple in delta_options_120_140:
                        delta_min, delta_max = delta_options_120_140[delta_tuple]
                elif bandera_140_160 == 1:
                     delta_tuple = (delta_min, delta_max)
                     if delta_tuple in delta_options_140_160:
                        delta_min, delta_max = delta_options_140_160[delta_tuple]
                elif bandera_160_180 == 1:
                     delta_tuple = (delta_min, delta_max)
                     if delta_tuple in delta_options_160_180:
                        delta_min, delta_max = delta_options_160_180[delta_tuple]
                elif bandera_180_200 == 1:
                     delta_tuple = (delta_min, delta_max)
                     if delta_tuple in delta_options_180_200:
                        delta_min, delta_max = delta_options_180_200[delta_tuple]
                elif bandera_200_220 == 1:
                     delta_tuple = (delta_min, delta_max)
                     if delta_tuple in delta_options_200_220:
                        delta_min, delta_max = delta_options_200_220[delta_tuple]
                elif bandera_220_240 == 1:
                     delta_tuple = (delta_min, delta_max)
                     if delta_tuple in delta_options_220_240:
                        delta_min, delta_max = delta_options_220_240[delta_tuple]
                elif bandera_240_260 == 1:
                     delta_tuple = (delta_min, delta_max)
                     if delta_tuple in delta_options_240_260:
                        delta_min, delta_max = delta_options_240_260[delta_tuple]
                elif bandera_260_280 == 1:
                     delta_tuple = (delta_min, delta_max)
                     if delta_tuple in delta_options_260_280:
                        delta_min, delta_max = delta_options_260_280[delta_tuple]                         
                elif bandera_280_300 == 1:
                     delta_tuple = (delta_min, delta_max)
                     if delta_tuple in delta_options_280_300:
                        delta_min, delta_max = delta_options_280_300[delta_tuple]
                elif bandera_300_320 == 1:
                     delta_tuple = (delta_min, delta_max)
                     if delta_tuple in delta_options_300_320:
                        delta_min, delta_max = delta_options_300_320[delta_tuple] 
                elif bandera_320_340 == 1:
                     delta_tuple = (delta_min, delta_max)
                     if delta_tuple in delta_options_320_340:
                        delta_min, delta_max = delta_options_320_340[delta_tuple]  
                elif bandera_340_360 == 1:
                     delta_tuple = (delta_min, delta_max)
                     if delta_tuple in delta_options_340_360:
                        delta_min, delta_max = delta_options_340_360[delta_tuple] 
                elif bandera_340_360 == 1:
                     delta_tuple = (delta_min, delta_max)
                     if delta_tuple in delta_options_340_360:
                        delta_min, delta_max = delta_options_340_360[delta_tuple]
                elif bandera_360_380 == 1:
                     delta_tuple = (delta_min, delta_max)
                     if delta_tuple in delta_options_360_380:
                        delta_min, delta_max = delta_options_360_380[delta_tuple]
                elif bandera_380_400 == 1:
                     delta_tuple = (delta_min, delta_max)
                     if delta_tuple in delta_options_380_400:
                        delta_min, delta_max = delta_options_380_400[delta_tuple]
                elif bandera_400_420 == 1:
                     delta_tuple = (delta_min, delta_max)
                     if delta_tuple in delta_options_400_420:
                        delta_min, delta_max = delta_options_400_420[delta_tuple]                          
                elif bandera_420_440 == 1:
                     delta_tuple = (delta_min, delta_max)
                     if delta_tuple in delta_options_420_440:
                        delta_min, delta_max = delta_options_420_440[delta_tuple]  
            i += 0.5    
    #starting to construct the output dataframe
    dcf_Results = pd.DataFrame(list_lndcf)
    dcf_Results = dcf_Results.rename({0 :"LNDCF_Max", 1 :"LNDCFERR", 2 :"EstimatedDelay", 3 :"bin", 4 :"delta min", 5 :"delta max", 6 :"True delay", 7 :"prep_technique", 8 :"error"}, axis='columns')
    dcf_Results = dcf_Results.drop(0)   
    min_value = dcf_Results["EstimatedDelay"].min()
    max_value = dcf_Results["EstimatedDelay"].max()
    uncertainty = (max_value - min_value) / 2 #calculate the uncertainty value  
    #convert to numeric each column
    dcf_Results['LNDCF_Max'] = pd.to_numeric(dcf_Results['LNDCF_Max'])
    dcf_Results['LNDCFERR'] = pd.to_numeric(dcf_Results['LNDCFERR'])
    dcf_Results['EstimatedDelay'] = pd.to_numeric(dcf_Results['EstimatedDelay'])
    dcf_Results['bin'] = pd.to_numeric(dcf_Results['bin'])
    dcf_Results['delta min'] = pd.to_numeric(dcf_Results['delta min'])
    dcf_Results['delta max'] = pd.to_numeric(dcf_Results['delta max'])
    dcf_Results['True delay'] = pd.to_numeric(dcf_Results['True delay'])
    dcf_Results['error'] = pd.to_numeric(dcf_Results['error'])
    #Search the minimum error or the closest delay estimation to the true or hint delay   
    minimumLastIdx = dcf_Results['error'].idxmin()
    min_row = pd.DataFrame(dcf_Results.loc[minimumLastIdx]).transpose().reset_index(drop=True)
    min_row.iloc[0, -2] = 'minimum error'
    #Search the maximum point of correlation and append to the ouput file    
    max_corelationIdx = dcf_Results["LNDCF_Max"].idxmax()
    max_corelationRow = pd.DataFrame(dcf_Results.loc[max_corelationIdx]).transpose().reset_index(drop=True)   
    max_corelationRow.iloc[0, -2] = 'max correlation' 
    #Calculate the mean of the minimum error or the closest delay estimation to the true or hint delay
    mean_row = pd.DataFrame({
    'LNDCF_Max':[dcf_Results["LNDCF_Max"].mean()],'LNDCFERR':[dcf_Results["LNDCFERR"].mean()],'EstimatedDelay':[dcf_Results["EstimatedDelay"].mean()],
    'bin': [dcf_Results["bin"].mean()],'delta min': [dcf_Results["delta min"].mean()], 'delta max': [dcf_Results["delta max"].mean()],
    'True delay': [dcf_Results["True delay"].mean()], 'prep_technique': [dcf_Results["prep_technique"]], 'error': [dcf_Results["error"].mean()]}) 
    mean_row.iloc[0, -2] = 'mean'
    mean_row.iloc[0, -1] = abs(mean_row["EstimatedDelay"] - mean_row["True delay"])  
    #Calculate the mode of the estimated delay and the other parameters
    mode_row = pd.DataFrame({
    'LNDCF_Max':[dcf_Results["LNDCF_Max"].mode().values[0]],'LNDCFERR':[dcf_Results["LNDCFERR"].mode().values[0]],'EstimatedDelay':[dcf_Results["EstimatedDelay"].mode().values[0]],
    'bin': [dcf_Results["bin"].mode().values[0]],'delta min': [dcf_Results["delta min"].mode().values[0]], 'delta max': [dcf_Results["delta max"].mode().values[0]],
    'True delay': [dcf_Results["True delay"].mode().values[0]], 'prep_technique': [dcf_Results["prep_technique"]], 'error': [dcf_Results["error"].mode().values[0]]}) 
    mode_row.iloc[0, -2] = 'mode'
    mode_row.iloc[0, -1] = abs(mode_row["EstimatedDelay"] - mode_row["True delay"])       
    #append rows 1.-min row, 2.- max point of correlation, 3.- mean of the estimated delay, 4.- mode of the estimated delay
    dcf_Results = dcf_Results.append(min_row, ignore_index=False)
    dcf_Results = dcf_Results.append(max_corelationRow, ignore_index=False)
    dcf_Results = dcf_Results.append(mean_row, ignore_index=False)
    dcf_Results = dcf_Results.append(mode_row, ignore_index=True)
    dcf_Results['uncertainty'] = pd.Series(uncertainty, index=dcf_Results.index)
    #format the output format of number of decimal  
    dcf_Results['LNDCF_Max'] = dcf_Results['LNDCF_Max'].map('{:,.5f}'.format)
    dcf_Results['LNDCFERR'] = dcf_Results['LNDCFERR'].map('{:,.5f}'.format)
    dcf_Results['EstimatedDelay'] = dcf_Results['EstimatedDelay'].map('{:,.2f}'.format)
    dcf_Results['bin'] = dcf_Results['bin'].map('{:,.1f}'.format)
    dcf_Results['delta min'] = dcf_Results['delta min'].map('{:,.1f}'.format)
    dcf_Results['delta max'] = dcf_Results['delta max'].map('{:,.1f}'.format)    
    dcf_Results['error'] = dcf_Results['error'].map('{:,.4f}'.format)
    #print(dcf_Results.head())
    #dcf_Results.to_csv("resultsLNDCF_" + prep_technique + ".csv", index=True, header=True)
    
    return dcf_Results





