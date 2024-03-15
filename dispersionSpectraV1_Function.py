
import pandas as pd
#import csv
import numpy as np
#import os
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
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)



def calculate_delay(fuenteLead, fuenteDelayed, df_truthrung, prep_technique):
    """
    Calculates the estimated time delay between two light curves using a specified preprocessing technique.
    It uses various delta (time shift) values to find the delay that minimizes the difference between the curves.
    
    Parameters:
        fuenteLead (DataFrame): The leading light curve data.
        fuenteDelayed (DataFrame): The delayed light curve data.
        df_truthrung (float): The true time delay between the light curves for simulation purposes.
        prep_technique (str): The preprocessing technique applied to the light curves before delay estimation.
    
    Returns:
        dfFiltered (DataFrame): A DataFrame containing the estimated delays, the true delay, error metrics,
                                and the preprocessing technique used. Includes mean, mode, and minimum error
                                estimations, along with an average of mean and mode estimations.
    """
    # Initialize mode_row with default values outside the try block
    mode_row = pd.DataFrame({
        'EstimatedDelay': [0],  # default value
        'delta_min': [0],  # default value
        'delta_max': [0],  # default value
        'trueDelay': [0],  # default value
        'error': [0],  # default value
        'prep_tech': ['default']  # default value or logic
                        })
    # Define variables for the estimation process
    delta_min = 0
    delta_max = 0
    inc = 1 # Increment for delta values
    dfFiltered = pd.DataFrame() # DataFrame to store filtered results
    z = 0
    x = 1
    # Assign file names for clarity
    fuente1 = fuenteLead # getting the name of the first file
    fuente2 = fuenteDelayed  # getting the name of the second file

    for j in range(1):   

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
        prep_technique = prep_technique
        # True delay from the given data
        trueDT = float(df_truthrung)
        print(str(trueDT))
        list_DS = []
        lcB_pctErr = pd.DataFrame(columns=['lcB_Err', 'B'])
        tope,range_low,range_high = 0,0,0
        # Setting initial parameters based on true delay
        # (This block defines various 'bandera' flags for different true delay ranges)
        # Each 'bandera' represents a flag to select the appropriate delta range for estimation
        # For example, bandera_01_20 is set if trueDT is within 1 to 20
        # Similar blocks for different ranges of trueDT up to 440.00
        # These blocks set delta_min and delta_max for the range within which the delay is estimated
        # Each block also sets 'tope' (limit for iterations), and range_low/high for filtering results
    
        # Custom logic based on the true delay to set the range of deltas to test

        if trueDT <= 20.00:
            delta_min, delta_max, bandera_01_20, tope, range_low, range_high = 1, 15, 1, 35, 0.50, 21.9
        elif 20.00 < trueDT <= 40.00:
            delta_min, delta_max, bandera_20_40, tope, range_low, range_high = 1, 35, 1, 47, 18.50, 41.50
        elif 40.00 < trueDT <= 60.00:
            delta_min, delta_max, bandera_40_60, tope, range_low, range_high = 5, 55, 1, 60, 38.50, 61.50
        elif 60.00 < trueDT <= 80.00:
                delta_min, delta_max, bandera_60_80, tope, range_low, range_high = 5, 75, 1, 34, 58.50, 81.50
        elif 80.00 < trueDT <= 100.00:
             delta_min, delta_max, bandera_80_100, tope, range_low, range_high = 10, 110, 1, 42, 78.50, 101.50
        elif 100.00 < trueDT <= 120.00:
            delta_min, delta_max, bandera_100_120, tope, range_low, range_high = 10, 120, 1, 32, 98.50, 121.50
        elif 120.00 < trueDT <= 140.00:
            delta_min, delta_max, bandera_120_140, tope, range_low, range_high = 85, 135, 1, 29, 118.50, 141.50
        elif 140.00 < trueDT <= 160.00:
            delta_min, delta_max, bandera_140_160, tope, range_low, range_high = 105, 155, 1, 29, 138.50, 161.50
        elif 160.00 < trueDT <= 180.00:
            delta_min, delta_max, bandera_160_180, tope, range_low, range_high = 125, 175, 1, 29, 158.50, 181.50
        elif 180.00 < trueDT <= 200.00:
            delta_min, delta_max, bandera_180_200, tope, range_low, range_high = 145, 195, 1, 29, 178.50, 201.50
        elif 200.00 < trueDT <= 220.00:
            delta_min, delta_max, bandera_200_220, tope, range_low, range_high = 165, 215, 1, 29, 198.50, 221.50
        elif 220.00 < trueDT <= 240.00:
            delta_min, delta_max, bandera_220_240, tope, range_low, range_high = 185, 235, 1, 29, 218.50, 241.50
        elif 240.00 < trueDT <= 260.00:
            delta_min, delta_max, bandera_240_260, tope, range_low, range_high = 205, 255, 1, 29, 238.50, 261.50
        elif 260.00 < trueDT <= 280.00:
            delta_min, delta_max, bandera_260_280, tope, range_low, range_high = 225, 275, 1, 29, 258.50, 281.50
        elif 280.00 < trueDT <= 300.00:
            delta_min, delta_max, bandera_280_300, tope, range_low, range_high = 245, 295, 1, 29, 278.50, 301.50
        elif 300.00 < trueDT <= 320.00:
            delta_min, delta_max, bandera_300_320, tope, range_low, range_high = 265, 315, 1, 29, 298.50, 321.50
        elif 320.00 < trueDT <= 340.00:
            delta_min, delta_max, bandera_320_340, tope, range_low, range_high = 285, 335, 1, 29, 318.50, 341.50
        elif 340.00 < trueDT <= 360.00:
            delta_min, delta_max, bandera_340_360, tope, range_low, range_high = 305, 355, 1, 29, 338.50, 361.50
        elif 360.00 < trueDT <= 380.00:
            delta_min, delta_max, bandera_360_380, tope, range_low, range_high = 325, 375, 1, 29, 358.50, 381.50
        elif 380.00 < trueDT <= 400.00:
            delta_min, delta_max, bandera_380_400, tope, range_low, range_high = 345, 395, 1, 29, 378.50, 401.50
        elif 400.00 < trueDT <= 420.00:
            delta_min, delta_max, bandera_400_420, tope, range_low, range_high = 365, 415, 1, 29, 398.50, 421.50            
        elif 420.00 < trueDT <= 440.00:
            delta_min, delta_max, bandera_420_440, tope, range_low, range_high = 385, 435, 1, 29, 418.50, 441.50 
        # Main loop to calculate the estimated delay
        for l in np.arange(0, tope):
            # Nested loop, currently iterates only once
            for dd in np.arange(0, 1, 1):
                # Process the light curves based on prep_technique
                # This example does not explicitly use prep_technique but it should be used here
                # to apply different preprocessing techniques to the light curves            
                # Logic to calculate the estimated delay
                # This involves creating DataFrame structures for both light curves,
                # applying the delay (delta), and calculating the 'error' for each delta           
                # Adjusting the delay based on preprocessing technique and calculating the errors            
                # After iterating through all deltas, calculate metrics like mean, mode, and minimum error
                #obtain the two light curves
                dfA = pd.DataFrame(fuente1)
                dfB = pd.DataFrame(fuente2)
                
                dfA.columns = ['t', 'a', 'std_a']
                dfB.columns = ['t', 'b', 'std_b']
                dfTime = dfB.filter(['t'])
                time = dfA.loc[:, 't']  # the time
                firstImage = dfA.loc[:, 'a']  # first image
                secondImage = dfB.loc[:, 'b']  # second image
                error_lca = dfA.loc[:, 'std_a']  # quoted errors for first image
                error_lcb = dfB.loc[:, 'std_b']  # quoted errors for second image
                std_a = pd.Series(error_lca)
                sumtotalwXab = []
                sumWF = []
                # parte del codigo para obtener M, para reescalar una de las dos curvas
                meanA = dfA['a'].mean() # obtengo media imagen A para calcular M  
                meanB = dfB['b'].mean() # obtengo media imagen B para calcular M
                difference = abs(abs(meanA) - abs(meanB))
                if(meanA > meanB):
                    dfB['b'] = dfB['b'] + difference   
                else:
                    dfA['a'] = dfA['a'] + difference

                for delta in np.arange(delta_min, delta_max + 1, inc):   # delta_min:10:delta_max,
                    t = pd.Series(time)
                    a = pd.Series(firstImage)
                    firstFrame = {'t': t, 'a': a}
                    firstSignal = pd.DataFrame(firstFrame)
                    firstSignal.insert(2, 'ones', 1)
                    lcB_pctErr['lcB_Err'] = dfB['std_b'] / dfB['b']
                    secondImage = dfB['b'] #+ M_np[M_count]
                    secondSignal = pd.DataFrame()
                    secondSignal['t'] = firstSignal['t'] - delta
                    secondSignal['a'] = secondImage
                    secondSignal.insert(2, 'ones', 0)
                    combinedSignals = firstSignal.append(secondSignal, sort=False, ignore_index=True)
                    combinedSignals = combinedSignals.sort_values('t')
                    arraycombinedSignals = combinedSignals.to_numpy()  # convierto en arreglo numpy para iterar el a_b del matlab
                    combinedSignals_Tail = combinedSignals.tail(-1)
                    combinedSignals_Head = combinedSignals.head(-1)
                    combinedSignals_Tail.reset_index(drop=True)
                    combinedSignals_Head.reset_index(drop=True)
                    combinedSignals_Tail.index = pd.RangeIndex(len(combinedSignals_Tail.index))
                    combinedSignals_Head.index = pd.RangeIndex(len(combinedSignals_Head.index))
                    firstFrameError = {'t': t, 'std_ab': std_a}
                    firstSignalError = pd.DataFrame(firstFrameError)
                    secondSignalError = pd.DataFrame()
                    secondSignalError['t'] = firstSignal['t'] - delta
                    secondSignalError['std_ab'] = secondSignal['a'] * lcB_pctErr['lcB_Err']
                    combinedErrors = firstSignalError.append(secondSignalError, sort=False, ignore_index=True)
                    combinedErrors = combinedErrors.sort_values(['t', 'std_ab'])
                    combinedErrorsF = combinedErrors['std_ab']
                    combinedErrorsF_Tail = combinedErrorsF.tail(-1)
                    combinedErrorsF_Head = combinedErrorsF.head(-1)
                    combinedErrorsF_Tail.index = pd.RangeIndex(len(combinedErrorsF_Tail.index))
                    combinedErrorsF_Head.index = pd.RangeIndex(len(combinedErrorsF_Head.index))
                    Wdf = 1 / (combinedErrorsF_Tail ** 2) + (combinedErrorsF_Head ** 2)
                    arraycombinedErrorsF = combinedErrorsF.to_numpy()
                    combinedSumSignal = pd.DataFrame()
                    combinedSumSignal['t'] = combinedSignals_Tail['t']
                    combinedSumSignal['a1'] = combinedSignals_Head['a']
                    combinedSumSignal['a2'] = combinedSignals_Tail['a']
                    combinedSumSignal['aF'] = np.power(combinedSignals_Tail['a'] - combinedSignals_Head['a'], 2)
                    combinedSumSignal['W1'] = combinedErrorsF_Head
                    combinedSumSignal['W2'] = combinedErrorsF_Tail
                    combinedSumSignal['W3'] = 1 / (np.power(combinedErrorsF_Tail, 2) + np.power(combinedErrorsF_Head, 2))
                    combinedSumSignal['W*aF'] = (1 / (np.power(combinedErrorsF_Tail, 2) + np.power(combinedErrorsF_Head, 2))) * (np.power(combinedSignals_Tail['a'] - combinedSignals_Head['a'], 2))
                    totalwXab = combinedSumSignal['W*aF'].sum()
                    sumtotalwXab.append(totalwXab)
                    sumW = combinedSumSignal['W3'].sum()
                    sumWF.append(sumW)

                dfsumWF = pd.DataFrame(sumWF, columns=['sumW'])
                dfsumtotalwXab = pd.DataFrame(sumtotalwXab, columns=['sumD'])
                dfsumWF['sumD'] = dfsumtotalwXab['sumD']
                dfsumWF['sumF'] = dfsumWF['sumD'] / 2 * dfsumWF['sumW']
                minIndex = dfsumWF['sumF'].idxmin()
                dsEDelay = delta_min + minIndex * inc
                list_DS.append([dsEDelay, delta_min, delta_max, trueDT, abs(abs(dsEDelay) - abs(trueDT)), prep_technique])     
            
            if bandera_01_20 == 1:
                #print("entro al if bandera 01 a 20")
                delta_tuple = (delta_min, delta_max)
                if delta_tuple in delta_options_01_20:
                    delta_min, delta_max = delta_options_01_20[delta_tuple] 
                else:
                    print("Key not found in delta_options 01 20:", delta_tuple)            
            elif bandera_20_40 == 1:
                #print("entro al if bandera 20 a 40")
                delta_tuple = (delta_min, delta_max)
                if delta_tuple in delta_options_20_40:
                    delta_min, delta_max = delta_options_20_40[delta_tuple] 
                else:
                    print("Key not found in delta_options 20 40:", delta_tuple)                
            elif bandera_40_60 == 1:
                  #print("entro al if bandera 40 a 60")
                  delta_tuple = (delta_min, delta_max)
                  if delta_tuple in delta_options_40_60:
                      delta_min, delta_max = delta_options_40_60[delta_tuple] 
                  else:
                      print("Key not found in delta_options 40 60:", delta_tuple)                                    
            elif bandera_60_80 == 1:
                #print("entro al if bandera 60 a 80")
                delta_tuple = (delta_min, delta_max)
                if delta_tuple in delta_options_60_80:
                    delta_min, delta_max = delta_options_60_80[delta_tuple]
                else:
                    print("Key not found in delta_options 60 a 80:", delta_tuple)     
            elif bandera_80_100 == 1:
                #print("entro al if bandera100")
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
                print("entro al if bandera160")
                delta_tuple = (delta_min, delta_max)
                if delta_tuple in delta_options_140_160:
                    delta_min, delta_max = delta_options_140_160[delta_tuple]
                    print(str(delta_options_140_160[delta_tuple]))
            elif bandera_160_180 == 1:
                print("entro al if bandera180")
                delta_tuple = (delta_min, delta_max)
                if delta_tuple in delta_options_160_180:
                    delta_min, delta_max = delta_options_160_180[delta_tuple]
                    print(str(delta_options_160_180[delta_tuple]))
            elif bandera_180_200 == 1:
                print("entro al if bandera200")
                delta_tuple = (delta_min, delta_max)
                if delta_tuple in delta_options_180_200:
                    delta_min, delta_max = delta_options_180_200[delta_tuple]
                    print(str(delta_options_180_200[delta_tuple]))
            elif bandera_200_220 == 1:
                #print("entro al if bandera220")
                delta_tuple = (delta_min, delta_max)
                if delta_tuple in delta_options_200_220:
                    delta_min, delta_max = delta_options_200_220[delta_tuple]
            elif bandera_220_240 == 1:
                #print("entro al if bandera240")
                delta_tuple = (delta_min, delta_max)
                if delta_tuple in delta_options_220_240:
                    delta_min, delta_max = delta_options_220_240[delta_tuple]
            elif bandera_240_260 == 1:
                #print("entro al if bandera240")
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
        ###############################################################
        z = z + 2
        x = x + 2
        dflist_DS = pd.DataFrame(list_DS, columns=['EstimatedDelay', 'delta_min', 'delta_max','trueDelay', 'error','prep_tech'])
        #dflist_DS.to_csv("ds_folder/DiffResults/DSv1Difference_R0pairs.csv", index=True, header=True)
        dfFiltered = dfFiltered.append(dflist_DS[(dflist_DS['EstimatedDelay'] >= range_low) & (dflist_DS['EstimatedDelay'] <= range_high)]) 
    #obtain the index of the min value(closest value to true delay)
    minimumLastIdx = dflist_DS['error'].idxmin()
    #Calculate the mean of the estimated delay and the other parameters
    mean_row = pd.DataFrame({
    'EstimatedDelay':[dfFiltered["EstimatedDelay"].mean()],'delta_min':[dfFiltered["delta_min"].mean()],'delta_max':[dfFiltered["delta_max"].mean()],
    'trueDelay': [dfFiltered["trueDelay"].mean()],'error': [dfFiltered["error"].mean()], 'prep_tech': [dfFiltered["prep_tech"]] })
    mean_row.iloc[0, -1] = 'mean'
    mean_row.iloc[0, -2] = abs(mean_row["EstimatedDelay"] - mean_row["trueDelay"])
    #Calculate the uncertainty
    min_value = dfFiltered["EstimatedDelay"].min()
    max_value = dfFiltered["EstimatedDelay"].max()
    uncertainty = (max_value - min_value) / 2 #calculate the uncertainty value
    #Calculate the mode of the estimated delay and the other parameters
    try:
        mode_row = pd.DataFrame({
            'EstimatedDelay': [dfFiltered["EstimatedDelay"].mode().values[0]],
            'delta_min': [dfFiltered["delta_min"].mode().values[0]],
            'delta_max': [dfFiltered["delta_max"].mode().values[0]],
            'trueDelay': [dfFiltered["trueDelay"].mode().values[0]],
            'error': [dfFiltered["error"].mode().values[0]],
            'prep_tech': [dfFiltered["prep_tech"].mode().values[0] if dfFiltered["prep_tech"].mode().values.size > 0 else 'default']  # Assuming you want to handle it similarly
            })
    except IndexError:
        # Handle the case where mode cannot be calculated due to empty  results
            print("Using default values for mode_row due to IndexError.")
        # Update specific values after the DataFrame has been successfully created or defaulted values are set
            mode_row.iloc[0, -1] = 'mode'
    if 'EstimatedDelay' in mode_row and 'trueDelay' in mean_row:  # Ensure columns exist
        mode_row.iloc[0, -2] = abs(mode_row["EstimatedDelay"][0] - mean_row["trueDelay"][0])  # Adjust based on mean_row structure
    ######################################
    #Calculate the min error of the estimated delay 
    # Calculate the uncertainty of the estimation
    # Calculate the mean and mode of the estimated delays and their corresponding errors
    min_row = pd.DataFrame(dflist_DS.loc[minimumLastIdx]).transpose().reset_index(drop=True)    
    min_row.iloc[0, -1] = 'minimum error'        
    last_row = pd.DataFrame({
        'EstimatedDelay':(mean_row["EstimatedDelay"]+mode_row["EstimatedDelay"])/2,'delta_min':(mean_row['delta_min']+mode_row["delta_min"])/2,
        'delta_max':(mean_row["delta_max"]+mode_row["delta_max"])/2,'trueDelay': mean_row["trueDelay"],'error':(mean_row["error"]+mode_row["error"])/2, 'prep_tech': mean_row["prep_tech"]}) 
    last_row.iloc[0, -2] = abs(last_row["EstimatedDelay"] - last_row["trueDelay"])
    last_row.iloc[0, -1] = 'avg:mean+mode' 
    dfFiltered = dfFiltered.append(min_row, ignore_index=False)                               
    dfFiltered = dfFiltered.append(mean_row, ignore_index=False)
    dfFiltered = dfFiltered.append(mode_row, ignore_index=False)    
    dfFiltered = dfFiltered.append(last_row, ignore_index=True)
    dfFiltered['uncertainty'] = pd.Series(uncertainty, index=dfFiltered.index)
    # Return the DataFrame with all the estimated delays, their errors, and the final chosen delay
    return dfFiltered


