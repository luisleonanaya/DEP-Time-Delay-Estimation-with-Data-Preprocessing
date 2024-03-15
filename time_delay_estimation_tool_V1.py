import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from export_to_pdf import export_histogram_and_stats_to_pdf
from tkinter.font import Font
import os
import pandas as pd
import numpy as np
from sys import platform
from skimage.restoration import (denoise_wavelet)
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import CFfilter_function
import rawData_function
import function_lndcf
import function_dcf_EK
import dispersionSpectraV1_Function
import data_differencing_function
import simpleNetReturn_function
import waveletDenoise_function
from PIL import Image, ImageTk
import scipy.stats as stats
from hurst import compute_Hc, random_walk
from scipy.stats import skew, kurtosis
from statsmodels.tsa.stattools import adfuller
import statsmodels.api as sm
import outputResults_DSv1
import outputResults_LNDCF
import outputResults_DCF
import frame_clear
from csv_saver import determine_and_save_csv
from dpi_awareness import set_dpi_awareness
from utilities import clear_frame, display_initial_image
# Call the function at the beginning for OS windows best look
set_dpi_awareness()
# Store the data for each series
series_data = {1: None, 2: None}
# Create two empy dataframes from posterior storage
dfA = pd.DataFrame()
dfB = pd.DataFrame()
hint_delay = None  # Initialize hint_delay as a global variable
frameStatistical_A = None
frameStatistical_B = None
canvasSecond = None
selected = None
input_value = None
radioButon_Selection = None
label_header_results = None
input_valueCombobox = None
banderaSearchRange = None
banderaKnownDelay = None
export_button = None
preprocessing_selectionAA = None
delayMethod_selectionAA = None
filteredRawData = None
DSv1RawData_SearchRange = None
filteredDiffData = None
DSv1DiffData_SearchRange = None
LNDCF_RawData_KD = None
LNDCF_RawData_SR = None
filteredSNR_Data = None
DSv1SNR_Data_SearchRange = None
filteredWD_Data = None
DSv1WD_Data_SearchRange = None
filteredWD2_Data = None
DSv1WD2_Data_SearchRange = None
filteredWD3_Data = None
DSv1WD3_Data_SearchRange = None
filteredCycle = None
filteredTrend = None
combined_df_CF_KD = None
combined_df_CF_SR = None
LNDCF_DiffData = None
LNDCF_DiffData_SR = None
LNDCF_SNR_Data = None
LNDCF_SNR_Data_SR = None
LNDCF_CFcycle_Data = None
LNDCF_CFtrend_Data = None
combined_df_LNDCF_CF_KD = None
combined_df_LNDCF_CF_SR = None
LNDCF_WD1_SR = None
LNDCF_WD1_KD = None
LNDCF_WD2_SR = None
LNDCF_WD2_KD = None
LNDCF_WD3_SR = None
LNDCF_WD3_KD = None
DCF_RawData = None
DCF_RawData_SR = None
DCF_DiffData_SR = None
DCF_DiffData = None
DCF_SNR_Data = None
DCF_SNR_Data_SR = None
DCF_CFcycle_Data = None
DCF_CFtrend_Data = None
combined_df_DCF_SR = None
combined_df_DFC_KD = None
DCF_WD1_KD = None
DCF_WD1_SR = None
DCF_WD2_KD = None
DCF_WD2_SR = None
DCF_WD3_KD = None
DCF_WD3_SR = None
figCFcycle_A = None
figCFcycle_B = None
formatted_output_lead_CF_cycle = None
formatted_output_delayed_CF_cycle = None
figCFtrend_A = None
figCFtrend_B = None
formatted_output_lead_CF_trend = None
formatted_output_delayed_CF_trend = None
figCF = None
df = None

"""
DEP: Time Delay Estimation with Data Preprocessing

This script initializes the graphical user interface for DEP, providing tools for uploading light curve data,
applying preprocessing techniques, visualizing light curves and their statistical attributes, and estimating time delays between light curves with various methodologies.

Usage:
- Run this script with Python 3.x.
- Follow the GUI prompts to upload light curve data files, select preprocessing options, and perform time delay estimations.
"""
########
# this dictionary is declared to pass as an argument to a external function to export results to csv file
global_vars = {
    'preprocessing_selectionAA': preprocessing_selectionAA,
    'delayMethod_selectionAA': delayMethod_selectionAA,
    'banderaKnownDelay': banderaKnownDelay,
    'banderaSearchRange': banderaSearchRange,
    'filteredRawData': filteredRawData,
    'filteredDiffData': filteredDiffData,
    'DSv1RawData_SearchRange': DSv1RawData_SearchRange,
    'DSv1DiffData_SearchRange': DSv1DiffData_SearchRange,
    'filteredSNR_Data': filteredSNR_Data,
    'DSv1SNR_Data_SearchRange': DSv1SNR_Data_SearchRange,
    'filteredWD_Data': filteredWD_Data,
    'DSv1WD_Data_SearchRange': DSv1WD_Data_SearchRange,
    'filteredWD2_Data': filteredWD2_Data,
    'DSv1WD2_Data_SearchRange': DSv1WD2_Data_SearchRange,
    'filteredWD3_Data': filteredWD3_Data,
    'DSv1WD3_Data_SearchRange': DSv1WD3_Data_SearchRange,
    'filteredWD3_Data': filteredWD3_Data,
    'DSv1WD3_Data_SearchRange': DSv1WD3_Data_SearchRange,
     'filteredCycle': filteredCycle,
     'filteredTrend': filteredTrend,
    'combined_df_CF_KD': combined_df_CF_KD,
     'combined_df_CF_SR': combined_df_CF_SR,
     'LNDCF_RawData_KD':  LNDCF_RawData_KD,
    'LNDCF_RawData_SR':  LNDCF_RawData_SR,
    'LNDCF_DiffData': LNDCF_DiffData,
     'LNDCF_DiffData_SR': LNDCF_DiffData_SR,
     'LNDCF_SNR_Data': LNDCF_SNR_Data,
     'LNDCF_SNR_Data_SR': LNDCF_SNR_Data_SR,
     'LNDCF_CFcycle_Data': LNDCF_CFcycle_Data,
     'LNDCF_CFtrend_Data': LNDCF_CFtrend_Data,
     'combined_df_LNDCF_CF_KD': combined_df_LNDCF_CF_KD,
      'combined_df_LNDCF_CF_SR': combined_df_LNDCF_CF_SR,
     'LNDCF_WD1_SR': LNDCF_WD1_SR,
     'LNDCF_WD1_KD': LNDCF_WD1_KD,
     'LNDCF_WD2_SR': LNDCF_WD2_SR,
     'LNDCF_WD2_KD': LNDCF_WD2_KD,
     'LNDCF_WD3_SR': LNDCF_WD3_SR,
     'LNDCF_WD3_KD': LNDCF_WD3_KD,
     'DCF_RawData': DCF_RawData,
     'DCF_RawData_SR': DCF_RawData_SR,
     'DCF_DiffData_SR': DCF_DiffData_SR,
     'DCF_DiffData': DCF_DiffData,
     'DCF_SNR_Data': DCF_SNR_Data,
     'DCF_SNR_Data_SR': DCF_SNR_Data_SR,
     'DCF_CFcycle_Data': DCF_CFcycle_Data,
     'DCF_CFtrend_Data': DCF_CFtrend_Data,
     'combined_df_DCF_SR': combined_df_DCF_SR,
     'combined_df_DFC_KD': combined_df_DFC_KD,
     'DCF_WD1_KD': DCF_WD1_KD,
     'DCF_WD1_SR': DCF_WD1_SR,
     'DCF_WD2_KD': DCF_WD2_KD,
     'DCF_WD2_SR': DCF_WD2_SR,
     'DCF_WD3_KD': DCF_WD3_KD,
     'DCF_WD3_SR': DCF_WD3_SR
}

# Create the main window
root = tk.Tk()
root.title("DEP: time Delay Estimation with data Preprocessing")

script_dir = os.path.dirname(os.path.realpath(__file__))
# Determine the icon file based on the operating system
if platform.startswith('win'):
    # Windows expects .png
    icon_path = os.path.join(script_dir, 'logo/Logo_UNAM.png')
elif platform.startswith('linux') or platform == 'darwin':  # 'darwin' is macOS
    # Linux and macOS expect .png
    icon_path = os.path.join(script_dir, 'logo/Logo_UNAM.png')
else:
    icon_path = None  # Default case for other OS, if any

if icon_path:
    try:
        # This works for PNG files on Linux, macOS, and Windows
        root.iconphoto(True, tk.PhotoImage(file=icon_path))
    except Exception as e:
        print(f"Failed to set the icon: {e}")

root.maxsize(2050, 1500)
root.grid_rowconfigure(0, weight=0)
root.grid_columnconfigure(0, weight=0)
root.resizable(False, False)
# Insert frame to display plots
framePlot_lcAB = tk.Frame(root, width=450, height=450)
framePlot_lcAB.grid(row=1, column=0, padx=3, pady=3)
# Insert frame to display results
frameResults = tk.Frame(root, width=50, height=25)
frameResults.pack_propagate(False)  # Prevents frame from resizing to fit the Treeview
frameResults.grid(row=3, column=0, padx=2, pady=2, sticky="n")
# Create a global treeview
global treeDisplay  # Declare treeDisplay as global
treeDisplay = ttk.Treeview(frameResults)  # Now you're working with the global variable
# Call function to display the initial image
display_initial_image(framePlot_lcAB)

# Function to handle file upload
def upload_file(series_num):
    """
    Allows the user to upload CSV or TXT files containing light curve data.
    The file should contain three numerical columns: time, magnitude, and magnitude error. First row is dismissed if it contains headers.
    Args:
        series_num (int): Identifier for the series of data being uploaded (1 for lead curve, 2 for delayed curve).
    """
    # Allow both CSV and TXT files, and ask the user to select a file
    file_path = filedialog.askopenfilename(filetypes=[("CSV and TXT files", "*.csv *.txt")])
    # Check if the user has cancelled the file selection
    if not file_path:
        messagebox.showinfo("Information", "File selection cancelled.")
        return
    # Check the file extension and set appropriate delimiter
    _, file_extension = os.path.splitext(file_path)
    if file_extension == '.csv':
        delimiter = ','
    elif file_extension == '.txt':
        delimiter = '\t'  # Change this based on the actual delimiter in your TXT files
    else:
        messagebox.showerror("Error", "Unsupported file format.")
        return

    try:
        # Attempt to read the file with the assumption it has no header
        df = pd.read_csv(file_path, header=None, delimiter=delimiter)
        # Check if the first row is numeric, if not, consider it a header and re-read the file
        if not pd.to_numeric(df.iloc[0], errors='coerce').notna().all():
            df = pd.read_csv(file_path, delimiter=delimiter)
        # Ensure the DataFrame has exactly three columns
        if df.shape[1] != 3:
            raise ValueError("The file must contain exactly three columns.")
        # Ensure all data is numeric
        if not df.applymap(lambda x: isinstance(x, (int, float))).all().all():
            raise ValueError("All columns must contain numerical data.")
        # Assign column names
        df.columns = ["time", "Magnitude", "error"]
        # Update the global variable with the new data
        global series_data
        series_data[series_num] = df

    except pd.errors.ParserError:
        messagebox.showerror("Error", "Error parsing the file. Please check the file format.")

    except ValueError as ve:
        messagebox.showerror("Error", str(ve))

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")
# Function to display results in the text area
def display_results():
    """
    Handles the process of collecting user inputs for delay estimation, initiates the computation of time delays between light curves using selected preprocessing and estimation methods, and displays the results in the GUI.

    This function acts as a central coordinator in the DEP application. It retrieves user-selected options for preprocessing and delay estimation methods, processes the uploaded light curve data according to these selections, computes the time delay, and updates the GUI with the results.

    Global Variables:
    - preprocessing_selectionAA (str): Indicates the preprocessing method chosen by the user.
    - delayMethod_selectionAA (str): Indicates the time delay estimation method chosen by the user.

    Workflow:
    1. Clears the results display frame for new output.
    2. Validates the user input for the known delay or the selected search range.
    3. Processes the uploaded light curve data according to the selected preprocessing method.
    4. Computes the time delay using the chosen delay estimation method.
    5. Displays the computed time delay and associated statistical data in the GUI's result section.

    Note:
    - This function interacts with multiple global variables that store user selections and data.
    - It relies on external functions for specific preprocessing steps and time delay computations.
    - Errors during file upload or processing are handled gracefully, with messages displayed to the user through the GUI.
    """
    # declarataion for use of global variables to use the export_to_pdf function
    global preprocessing_selectionAA
    global delayMethod_selectionAA
    global filteredRawData
    global filteredDiffData
    global DSv1RawData_SearchRange
    global DSv1DiffData_SearchRange
    global LNDCF_RawData_KD
    global LNDCF_RawData_SR
    global filteredSNR_Data
    global DSv1SNR_Data_SearchRange
    global filteredWD_Data
    global DSv1WD_Data_SearchRange
    global filteredWD2_Data
    global DSv1WD2_Data_SearchRange
    global filteredWD3_Data
    global DSv1WD3_Data_SearchRange
    global filteredCycle
    global filteredTrend
    global combined_df_CF_KD
    global combined_df_CF_SR
    global LNDCF_DiffData
    global LNDCF_DiffData_SR
    global LNDCF_SNR_Data
    global LNDCF_SNR_Data_SR
    global LNDCF_CFcycle_Data
    global LNDCF_CFtrend_Data
    global combined_df_LNDCF_CF_KD
    global combined_df_LNDCF_CF_SR
    global LNDCF_WD1_SR
    global LNDCF_WD1_KD
    global LNDCF_WD2_SR
    global LNDCF_WD2_KD
    global LNDCF_WD3
    global LNDCF_WD3_SR
    global LNDCF_WD3_KD
    global DCF_RawData
    global DCF_RawData_SR
    global DCF_DiffData_SR
    global DCF_DiffData
    global DCF_SNR_Data
    global DCF_SNR_Data_SR
    global DCF_CFcycle_Data
    global DCF_CFtrend_Data
    global combined_df_DCF_SR
    global combined_df_DFC_KD
    global DCF_WD1_KD
    global DCF_WD1_SR
    global DCF_WD2_KD
    global DCF_WD2_SR
    global DCF_WD3_KD
    global DCF_WD3_SR
    global banderaSearchRange
    global banderaKnownDelay
    global hint_delay
    # Clear content in every function call for the statstistical analisys output frames
    if frameResults is not None:
        frame_clear.clear_frame(frameResults)
    selected = radioButon_Selection.get()
    # print(selected)
    if selected == 0:
        delayLabel.config(text="Error: zero is not valid input")
        return
    if selected == 1:
        input_value = delayEntry.get()
        check_delay = float(input_value)
        if check_delay > 440:
           delayLabel.config(text="Error: Input is to high")
           return
        elif check_delay < 0.1:
           delayLabel.config(text="Error: Input must be a positive")
           return

        try:
            hint_delay = float(input_value)
            delayLabel.config(text=f"Inserted value is : {hint_delay}")
            banderaKnownDelay = 1
            banderaSearchRange = 0
        except ValueError:
            # Handle the ValueError (invalid float input)
            if input_value.strip() == "":
                delayLabel.config(text="Error: Input is empty")
                return
            elif input_value.strip() == " ":
                delayLabel.config(text="Error: Input is empty")
                return
            else:
                delayLabel.config(text=f"Error: '{input_value}' is not a valid float")
                return
    elif selected == 2:
        input_valueCombobox = timeDelay_range_search.get()
        if input_valueCombobox != "Select range":
            delayLabel.config(text=f"Search range : '{input_valueCombobox}'")
            if input_valueCombobox == "1 to 20":
                input_value = 10.00
                hint_delay = float(input_value)
                banderaSearchRange = 1
                banderaKnownDelay = 0
            elif input_valueCombobox == "20 to 40":
                input_value = 30.00
                hint_delay = float(input_value)
                banderaSearchRange = 1
                banderaKnownDelay = 0
            elif input_valueCombobox == "40 to 60":
                input_value = 50.00
                hint_delay = float(input_value)
                banderaSearchRange = 1
                banderaKnownDelay = 0
            elif input_valueCombobox == "60 to 80":
                input_value = 70.00
                hint_delay = float(input_value)
                banderaSearchRange = 1
                banderaKnownDelay = 0
            elif input_valueCombobox == "80 to 100":
                input_value = 90.00
                hint_delay = float(input_value)
                banderaSearchRange = 1
                banderaKnownDelay = 0
            elif input_valueCombobox == "100 to 120":
                input_value = 110.00
                hint_delay = float(input_value)
                banderaSearchRange = 1
                banderaKnownDelay = 0
            elif input_valueCombobox == "120 to 140":
                input_value = 130.00
                hint_delay = float(input_value)
                banderaSearchRange = 1
                banderaKnownDelay = 0
            elif input_valueCombobox == "140 to 160":
                input_value = 150.00
                hint_delay = float(input_value)
                banderaSearchRange = 1
                banderaKnownDelay = 0
            elif input_valueCombobox == "160 to 180":
                input_value = 170.00
                hint_delay = float(input_value)
                banderaSearchRange = 1
                banderaKnownDelay = 0
            elif input_valueCombobox == "160 to 180":
                input_value = 170.00
                hint_delay = float(input_value)
                banderaSearchRange = 1
                banderaKnownDelay = 0
            elif input_valueCombobox == "180 to 200":
                input_value = 190.00
                hint_delay = float(input_value)
                banderaSearchRange = 1
                banderaKnownDelay = 0
            elif input_valueCombobox == "200 to 220":
                input_value = 210.00
                hint_delay = float(input_value)
                banderaSearchRange = 1
                banderaKnownDelay = 0
            elif input_valueCombobox == "220 to 240":
                input_value = 230.00
                hint_delay = float(input_value)
                banderaSearchRange = 1
                banderaKnownDelay = 0
            elif input_valueCombobox == "240 to 260":
                input_value = 250.00
                hint_delay = float(input_value)
                banderaSearchRange = 1
                banderaKnownDelay = 0
            elif input_valueCombobox == "260 to 280":
                input_value = 270.00
                hint_delay = float(input_value)
                banderaSearchRange = 1
                banderaKnownDelay = 0
            elif input_valueCombobox == "280 to 300":
                input_value = 290.00
                hint_delay = float(input_value)
                banderaSearchRange = 1
                banderaKnownDelay = 0
            elif input_valueCombobox == "300 to 320":
                input_value = 310.00
                hint_delay = float(input_value)
                banderaSearchRange = 1
                banderaKnownDelay = 0
            elif input_valueCombobox == "320 to 340":
                input_value = 330.00
                hint_delay = float(input_value)
                banderaSearchRange = 1
                banderaKnownDelay = 0
            elif input_valueCombobox == "340 to 360":
                input_value = 350.00
                hint_delay = float(input_value)
                banderaSearchRange = 1
                banderaKnownDelay = 0
            elif input_valueCombobox == "360 to 380":
                input_value = 370.00
                hint_delay = float(input_value)
                banderaSearchRange = 1
                banderaKnownDelay = 0
            elif input_valueCombobox == "380 to 400":
                input_value = 390.00
                hint_delay = float(input_value)
                banderaSearchRange = 1
                banderaKnownDelay = 0
            elif input_valueCombobox == "400 to 420":
                input_value = 410.00
                hint_delay = float(input_value)
                banderaSearchRange = 1
                banderaKnownDelay = 0
            elif input_valueCombobox == "420 to 440":
                input_value = 430.00
                hint_delay = float(input_value)
                banderaSearchRange = 1
                banderaKnownDelay = 0
        else:
            delayLabel.config(text="Select a valid input")
            return
        # 1 to 20", "20 to 40", "40 to 60",
    try:
        dfA = series_data[1].copy()
        dfB = series_data[2].copy()
    except AttributeError as e:
        # Handle the error and return a message to the user
        error_message = "An error occurred: data is empty."
        delayLabel.config(text=error_message)
        # Return a message to the user
        return error_message

    dfA.rename(columns={"Julian_day": "time", "Magnitude": "lc_A", "error": "err_A"}, inplace=True)
    # dfLights['lcA_pctErr'] = dfLights['lc_AErr'] / dfLights['lc_A']
    dfA['pctErr_A'] = dfA['err_A'] / dfA['lc_A']
    dfB.rename(columns={"Julian_day": "time", "Magnitude": "lc_B", "error": "err_B"}, inplace=True)
    dfB['pctErr_B'] = dfB['err_B'] / dfB['lc_B']

    preprocessing_selectionAA = preprocessing_selection.get()
    delayMethod_selectionAA = delayMethod_selection.get()

    if preprocessing_selectionAA == "Christiano-Fitzgerald filter" and delayMethod_selectionAA == "Dispersion Spectra":
        prep_techniqueA = "CF-trend"
        prep_techniqueB = "CF-cycle"
        dfCycle_lcA, dfCycle_lcB, dfTrend_lcA, dfTrend_lcB = CFfilter_function.cf_filter(dfA, dfB, hint_delay)
        # calculate trend of CF filter
        filteredCycle = dispersionSpectraV1_Function.calculate_delay(dfCycle_lcA, dfCycle_lcB, hint_delay, prep_techniqueB)
        filteredTrend = dispersionSpectraV1_Function.calculate_delay(dfTrend_lcA, dfTrend_lcB, hint_delay, prep_techniqueA)

        if banderaKnownDelay == 1:
            # obtain the last four rows from cycle
            last_fourth_cycle_rows = filteredCycle.iloc[-4:]
            row_one_min_cycle_preantepenultimate = last_fourth_cycle_rows.iloc[0]  # get first row
            row_two_mean_cycle_antepenultimate = last_fourth_cycle_rows.iloc[1]  # get second row
            row_three_mode_cycle_penultimate = last_fourth_cycle_rows.iloc[2]  # get third row
            row_four_avg_cycle_last = last_fourth_cycle_rows.iloc[3]  # get fourth row
            # obtain the last four rows from trend
            last_fourth_trend_rows = filteredTrend.iloc[-4:]
            row_one_min_trend_preantepenultimate = last_fourth_trend_rows.iloc[0]  # get first row
            row_two_mean_trend_antepenultimate = last_fourth_trend_rows.iloc[1]  # get second row
            row_three_mode_trend_penultimate = last_fourth_trend_rows.iloc[2]  # get third row
            row_four_avg_trend_last = last_fourth_trend_rows.iloc[3]  # get fourth row
            # Calculate the combined min error
            min_error_row_Combined = pd.DataFrame({
                'EstimatedDelay': (row_one_min_cycle_preantepenultimate["EstimatedDelay"] +
                                   row_one_min_trend_preantepenultimate["EstimatedDelay"]) / 2,
                'delta_min': (row_one_min_cycle_preantepenultimate['delta_min'] + row_one_min_trend_preantepenultimate[
                    "delta_min"]) / 2,
                'delta_max': (row_one_min_cycle_preantepenultimate["delta_max"] + row_one_min_trend_preantepenultimate[
                    "delta_max"]) / 2,
                'trueDelay': row_one_min_cycle_preantepenultimate["trueDelay"],
                'error': abs(((row_one_min_cycle_preantepenultimate["EstimatedDelay"] +
                               row_one_min_trend_preantepenultimate["EstimatedDelay"]) / 2) -
                          row_one_min_cycle_preantepenultimate["trueDelay"]),
                'prep_tech': row_one_min_cycle_preantepenultimate["prep_tech"],
                'uncertainty': (row_one_min_cycle_preantepenultimate['uncertainty'] +
                                row_one_min_trend_preantepenultimate['uncertainty']) / 2}, index=[0])
            min_error_row_Combined.iloc[0, -2] = 'min trend/cycle'
            # Calculate the combined mean
            mean_error_row_Combined = pd.DataFrame({
                'EstimatedDelay': (row_two_mean_cycle_antepenultimate["EstimatedDelay"] +
                                   row_two_mean_trend_antepenultimate["EstimatedDelay"]) / 2,
                'delta_min': (row_two_mean_cycle_antepenultimate['delta_min'] + row_two_mean_trend_antepenultimate["delta_min"]) / 2,
                'delta_max': (row_two_mean_cycle_antepenultimate["delta_max"] + row_two_mean_trend_antepenultimate["delta_max"]) / 2,
                'trueDelay': row_two_mean_cycle_antepenultimate["trueDelay"],
                'error': abs(((row_two_mean_cycle_antepenultimate["EstimatedDelay"] +
                               row_two_mean_trend_antepenultimate["EstimatedDelay"]) / 2) -
                          row_two_mean_cycle_antepenultimate["trueDelay"]),
                'prep_tech': row_two_mean_cycle_antepenultimate["prep_tech"],
                'uncertainty': (row_two_mean_cycle_antepenultimate['uncertainty'] + row_two_mean_trend_antepenultimate['uncertainty']) / 2}, index=[0])
            mean_error_row_Combined.iloc[0, -2] = 'mean trend/cycle'
            # Calculate the combined mode
            mode_error_row_Combined = pd.DataFrame({
                'EstimatedDelay': (row_three_mode_cycle_penultimate["EstimatedDelay"] +
                                   row_three_mode_trend_penultimate["EstimatedDelay"]) / 2,
                'delta_min': (row_three_mode_cycle_penultimate['delta_min'] + row_three_mode_trend_penultimate["delta_min"]) / 2,
                'delta_max': (row_three_mode_cycle_penultimate["delta_max"] + row_three_mode_trend_penultimate["delta_max"]) / 2,
                'trueDelay': row_three_mode_cycle_penultimate["trueDelay"],
                'error': abs(((row_three_mode_cycle_penultimate["EstimatedDelay"] + row_three_mode_trend_penultimate[
                    "EstimatedDelay"]) / 2) - row_three_mode_cycle_penultimate["trueDelay"]),
                'prep_tech': row_three_mode_cycle_penultimate["prep_tech"],
                'uncertainty': (row_three_mode_cycle_penultimate['uncertainty'] + row_three_mode_trend_penultimate['uncertainty']) / 2}, index=[0])
            mode_error_row_Combined.iloc[0, -2] = 'mode trend/cycle'
            # Calculate the average of the combined mean and mode
            last_error_row_Combined = pd.DataFrame({
                'EstimatedDelay': (row_four_avg_cycle_last["EstimatedDelay"] + row_four_avg_trend_last[
                    "EstimatedDelay"]) / 2,
                'delta_min': (row_four_avg_cycle_last['delta_min'] + row_four_avg_trend_last["delta_min"]) / 2,
                'delta_max': (row_four_avg_cycle_last["delta_max"] + row_four_avg_trend_last["delta_max"]) / 2,
                'trueDelay': row_four_avg_cycle_last["trueDelay"],
                'error': abs(((row_four_avg_cycle_last["EstimatedDelay"] + row_four_avg_trend_last[
                    "EstimatedDelay"]) / 2) - row_four_avg_cycle_last["trueDelay"]),
                'prep_tech': row_four_avg_cycle_last["prep_tech"],
                'uncertainty': (row_four_avg_cycle_last['uncertainty'] + row_four_avg_trend_last['uncertainty']) / 2},index=[0])
            last_error_row_Combined.iloc[0, -2] = 'avg mean+mode trend/cycle'
                        # Create a header to insert to the concatenated DataFrames
            header1 = pd.DataFrame([{'EstimatedDelay': 'EstimatedDelay', 'delta_min': 'delta_min',
                                     'delta_max': 'delta_max', 'trueDelay': 'trueDelay', 'error': 'error',
                                     'prep_tech': 'prep_tech', 'uncertainty': 'uncertainty'}])
            # Ensure that the following columns are numeric for format output
            filteredTrend['EstimatedDelay'] = pd.to_numeric(filteredTrend['EstimatedDelay'], errors='coerce')
            filteredTrend['delta_min'] = pd.to_numeric(filteredTrend['delta_min'], errors='coerce')
            filteredTrend['delta_max'] = pd.to_numeric(filteredTrend['delta_max'], errors='coerce')
            filteredTrend['uncertainty'] = pd.to_numeric(filteredTrend['uncertainty'], errors='coerce')
            filteredTrend['error'] = pd.to_numeric(filteredTrend['error'], errors='coerce')
            # Ensure that the following columns are numeric for format output
            filteredCycle['EstimatedDelay'] = pd.to_numeric(filteredCycle['EstimatedDelay'], errors='coerce')
            filteredCycle['delta_min'] = pd.to_numeric(filteredCycle['delta_min'], errors='coerce')
            filteredCycle['delta_max'] = pd.to_numeric(filteredCycle['delta_max'], errors='coerce')
            filteredCycle['uncertainty'] = pd.to_numeric(filteredCycle['uncertainty'], errors='coerce')
            filteredCycle['error'] = pd.to_numeric(filteredCycle['error'], errors='coerce')
            # Ensure that the following columns are numeric for format output
            min_error_row_Combined['EstimatedDelay'] = pd.to_numeric(min_error_row_Combined['EstimatedDelay'], errors='coerce')
            min_error_row_Combined['delta_min'] = pd.to_numeric(min_error_row_Combined['delta_min'], errors='coerce')
            min_error_row_Combined['delta_max'] = pd.to_numeric(min_error_row_Combined['delta_max'], errors='coerce')
            min_error_row_Combined['uncertainty'] = pd.to_numeric(min_error_row_Combined['uncertainty'], errors='coerce')
            min_error_row_Combined['error'] = pd.to_numeric(min_error_row_Combined['error'], errors='coerce')
            # Ensure that the following columns are numeric for format output
            mean_error_row_Combined['EstimatedDelay'] = pd.to_numeric(mean_error_row_Combined['EstimatedDelay'], errors='coerce')
            mean_error_row_Combined['delta_min'] = pd.to_numeric(mean_error_row_Combined['delta_min'], errors='coerce')
            mean_error_row_Combined['delta_max'] = pd.to_numeric(mean_error_row_Combined['delta_max'], errors='coerce')
            mean_error_row_Combined['uncertainty'] = pd.to_numeric(mean_error_row_Combined['uncertainty'], errors='coerce')
            mean_error_row_Combined['error'] = pd.to_numeric(mean_error_row_Combined['error'], errors='coerce')
            # Ensure that the following columns are numeric for format output
            mode_error_row_Combined['EstimatedDelay'] = pd.to_numeric(mode_error_row_Combined['EstimatedDelay'], errors='coerce')
            mode_error_row_Combined['delta_min'] = pd.to_numeric(mode_error_row_Combined['delta_min'], errors='coerce')
            mode_error_row_Combined['delta_max'] = pd.to_numeric(mode_error_row_Combined['delta_max'], errors='coerce')
            mode_error_row_Combined['uncertainty'] = pd.to_numeric(mode_error_row_Combined['uncertainty'], errors='coerce')
            mode_error_row_Combined['error'] = pd.to_numeric(mode_error_row_Combined['error'], errors='coerce')
            # Ensure that the following columns are numeric for format output
            last_error_row_Combined['EstimatedDelay'] = pd.to_numeric(last_error_row_Combined['EstimatedDelay'], errors='coerce')
            last_error_row_Combined['delta_min'] = pd.to_numeric(last_error_row_Combined['delta_min'], errors='coerce')
            last_error_row_Combined['delta_max'] = pd.to_numeric(last_error_row_Combined['delta_max'], errors='coerce')
            last_error_row_Combined['uncertainty'] = pd.to_numeric(last_error_row_Combined['uncertainty'], errors='coerce')
            last_error_row_Combined['error'] = pd.to_numeric(last_error_row_Combined['error'], errors='coerce')
            #######################################
            # Transform panda dataframe row to panda series to properly work as input in the display function
            row_one_preantepenultimate = min_error_row_Combined.iloc[0]  # get first row
            row_two_antepenultimate = mean_error_row_Combined.iloc[0]  # get second row
            row_three_penultimate = mode_error_row_Combined.iloc[0]  # get third row
            row_four_last = last_error_row_Combined.iloc[0]  # get fourth row
            ##call fucntion to display the results
            outputResults_DSv1.display_DSV1_results_knownDelay(frameResults, row_one_preantepenultimate, row_two_antepenultimate, row_three_penultimate, row_four_last)
            # The next piece of code is for creating the output csv file
            # Define the format for numeric columns
            qty_decimals = '{:.4f}'  # Choosed the number of four decimal places
            # Apply formatting to specific numeric columns
            floatingc_columns = ['EstimatedDelay', 'delta_min', 'delta_max', 'uncertainty', 'error']
            filteredTrend[floatingc_columns] = filteredTrend[floatingc_columns].applymap(lambda x: qty_decimals.format(x))
            filteredCycle[floatingc_columns] = filteredCycle[floatingc_columns].applymap(lambda x: qty_decimals.format(x))
            ##
            min_error_row_Combined[floatingc_columns] = min_error_row_Combined[floatingc_columns].applymap(lambda x: qty_decimals.format(x))
            mean_error_row_Combined[floatingc_columns] = mean_error_row_Combined[floatingc_columns].applymap(lambda x: qty_decimals.format(x))
            mode_error_row_Combined[floatingc_columns] = mode_error_row_Combined[floatingc_columns].applymap(lambda x: qty_decimals.format(x))
            last_error_row_Combined[floatingc_columns] = last_error_row_Combined[floatingc_columns].applymap(lambda x: qty_decimals.format(x))
            # first concataneion of the dataframes
            combined_df_A = pd.concat([filteredTrend, header1, filteredCycle, header1], ignore_index=True)
            # concatanate the last four rows of the file
            combined_df_B = min_error_row_Combined.append([mean_error_row_Combined, mode_error_row_Combined, last_error_row_Combined], ignore_index=True)
            # second concatenation
            combined_df_CF_KD = pd.concat([combined_df_A, combined_df_B], ignore_index=True)
            banderaSearchRange = 0
            # convert the dataframes concateneted to an output file in csv
            #combined_df_C.to_csv("resultsDSv1_CF_cycle_trend_KnownDelay.csv", header=True, index=True)

        elif banderaSearchRange == 1:
            # Create the cycle dataframe with new headers to drop the unwanted error row and error column
            DSv1CF_cycle_SearchRange = filteredCycle
            DSv1CF_cycle_SearchRange.columns = ['Estimated Delay', 'delta min', 'delta max', 'search range', 'error',
                                                'prep_technique', 'uncertainty']
            DSv1CF_cycle_SearchRange.drop('error', axis=1, inplace=True)
            DSv1CF_cycle_SearchRange.drop(DSv1CF_cycle_SearchRange.index[-4], axis=0, inplace=True)
            # Insert search range for cycle
            DSv1CF_cycle_SearchRange['search range'] = DSv1CF_cycle_SearchRange['search range'].apply(
                lambda x: str(input_valueCombobox))
            # Create the trend dataframe with new headers to drop the unwanted error row and error column
            DSv1CF_trend_SearchRange = filteredTrend
            DSv1CF_trend_SearchRange.columns = ['Estimated Delay', 'delta min', 'delta max', 'search range', 'error',
                                                'prep_technique', 'uncertainty']
            DSv1CF_trend_SearchRange.drop('error', axis=1, inplace=True)
            DSv1CF_trend_SearchRange.drop(DSv1CF_trend_SearchRange.index[-4], axis=0, inplace=True)
            # Insert search range for trend
            DSv1CF_trend_SearchRange['search range'] = DSv1CF_trend_SearchRange['search range'].apply(
                lambda x: str(input_valueCombobox))
            # obtain the last Three rows from cycle
            last_three_cycle_rows = DSv1CF_cycle_SearchRange.iloc[-3:]
            row_one_mean_cycle_antepenultimate = last_three_cycle_rows.iloc[0]  # get second row
            row_two_mode_cycle_penultimate = last_three_cycle_rows.iloc[1]  # get third row
            row_three_avg_cycle_last = last_three_cycle_rows.iloc[2]  # get fourth row
            # obtain the last four rows from trend
            last_three_trend_rows = DSv1CF_trend_SearchRange.iloc[-3:]
            row_one_mean_trend_antepenultimate = last_three_trend_rows.iloc[0]  # get second row
            row_two_mode_trend_penultimate = last_three_trend_rows.iloc[1]  # get third row
            row_three_avg_trend_last = last_three_trend_rows.iloc[2]  # get fourth row
            # Calculate the combined mean
            mean_error_row_Combined = pd.DataFrame({
                'Estimated Delay': (row_one_mean_cycle_antepenultimate["Estimated Delay"] +
                                    row_one_mean_trend_antepenultimate["Estimated Delay"]) / 2,
                'delta min': (row_one_mean_cycle_antepenultimate['delta min'] + row_one_mean_trend_antepenultimate["delta min"]) / 2,
                'delta max': (row_one_mean_cycle_antepenultimate["delta max"] + row_one_mean_trend_antepenultimate["delta max"]) / 2,
                'search range': row_one_mean_cycle_antepenultimate["search range"],
                'prep_technique': row_one_mean_cycle_antepenultimate["prep_technique"],
                'uncertainty': (row_one_mean_cycle_antepenultimate['uncertainty'] + row_one_mean_trend_antepenultimate['uncertainty']) / 2}, index=[0])
            mean_error_row_Combined.iloc[0, -2] = 'mean trend/cycle'
            # Calculate the combined mode
            mode_error_row_Combined = pd.DataFrame({
                'Estimated Delay': (row_two_mode_cycle_penultimate["Estimated Delay"] + row_two_mode_trend_penultimate["Estimated Delay"]) / 2,
                'delta min': (row_two_mode_cycle_penultimate['delta min'] + row_two_mode_trend_penultimate["delta min"]) / 2,
                'delta max': (row_two_mode_cycle_penultimate["delta max"] + row_two_mode_trend_penultimate["delta max"]) / 2,
                'search range': row_two_mode_cycle_penultimate["search range"],
                'prep_technique': row_two_mode_cycle_penultimate["prep_technique"],
                'uncertainty': (row_two_mode_cycle_penultimate['uncertainty'] + row_two_mode_trend_penultimate['uncertainty']) / 2}, index=[0])
            mode_error_row_Combined.iloc[0, -2] = 'mode trend/cycle'
            # Calculate the average of the combined mean and mode
            last_error_row_Combined = pd.DataFrame({
                'Estimated Delay': (row_three_avg_cycle_last["Estimated Delay"] + row_three_avg_trend_last[
                    "Estimated Delay"]) / 2,
                'delta min': (row_three_avg_cycle_last['delta min'] + row_three_avg_trend_last["delta min"]) / 2,
                'delta max': (row_three_avg_cycle_last["delta max"] + row_three_avg_trend_last["delta max"]) / 2,
                'search range': row_three_avg_cycle_last["search range"],
                'prep_technique': row_three_avg_cycle_last["prep_technique"],
                'uncertainty': (row_three_avg_cycle_last['uncertainty'] + row_three_avg_trend_last['uncertainty']) / 2}, index=[0])
            last_error_row_Combined.iloc[0, -2] = 'avg mean+mode trend/cycle'
            # Create a header to insert to the concatenated DataFrames
            header1 = pd.DataFrame([{'Estimated Delay': 'Estimated Delay', 'delta min': 'delta min',
                                     'delta max': 'delta max', 'search range': 'search range',
                                     'prep_technique': 'prep_technique', 'uncertainty': 'uncertainty'}])
            # Ensure that the following columns are numeric for format output
            DSv1CF_cycle_SearchRange['Estimated Delay'] = pd.to_numeric(DSv1CF_cycle_SearchRange['Estimated Delay'], errors='coerce')
            DSv1CF_cycle_SearchRange['delta min'] = pd.to_numeric(DSv1CF_cycle_SearchRange['delta min'], errors='coerce')
            DSv1CF_cycle_SearchRange['delta max'] = pd.to_numeric(DSv1CF_cycle_SearchRange['delta max'], errors='coerce')
            DSv1CF_cycle_SearchRange['uncertainty'] = pd.to_numeric(DSv1CF_cycle_SearchRange['uncertainty'], errors='coerce')
            # Ensure that the following columns are numeric for format output
            DSv1CF_trend_SearchRange['Estimated Delay'] = pd.to_numeric(DSv1CF_trend_SearchRange['Estimated Delay'], errors='coerce')
            DSv1CF_trend_SearchRange['delta min'] = pd.to_numeric(DSv1CF_trend_SearchRange['delta min'], errors='coerce')
            DSv1CF_trend_SearchRange['delta max'] = pd.to_numeric(DSv1CF_trend_SearchRange['delta max'], errors='coerce')
            DSv1CF_trend_SearchRange['uncertainty'] = pd.to_numeric(DSv1CF_trend_SearchRange['uncertainty'], errors='coerce')
            # Ensure that the following columns are numeric for format output
            mean_error_row_Combined['Estimated Delay'] = pd.to_numeric(mean_error_row_Combined['Estimated Delay'], errors='coerce')
            mean_error_row_Combined['delta min'] = pd.to_numeric(mean_error_row_Combined['delta min'], errors='coerce')
            mean_error_row_Combined['delta max'] = pd.to_numeric(mean_error_row_Combined['delta max'], errors='coerce')
            mean_error_row_Combined['uncertainty'] = pd.to_numeric(mean_error_row_Combined['uncertainty'], errors='coerce')
            # Ensure that the following columns are numeric for format output
            mode_error_row_Combined['Estimated Delay'] = pd.to_numeric(mode_error_row_Combined['Estimated Delay'], errors='coerce')
            mode_error_row_Combined['delta min'] = pd.to_numeric(mode_error_row_Combined['delta min'], errors='coerce')
            mode_error_row_Combined['delta max'] = pd.to_numeric(mode_error_row_Combined['delta max'], errors='coerce')
            mode_error_row_Combined['uncertainty'] = pd.to_numeric(mode_error_row_Combined['uncertainty'], errors='coerce')
            # Ensure that the following columns are numeric for format output
            last_error_row_Combined['Estimated Delay'] = pd.to_numeric(last_error_row_Combined['Estimated Delay'], errors='coerce')
            last_error_row_Combined['delta min'] = pd.to_numeric(last_error_row_Combined['delta min'], errors='coerce')
            last_error_row_Combined['delta max'] = pd.to_numeric(last_error_row_Combined['delta max'], errors='coerce')
                        #######################################
            # Transform panda dataframe row to panda series to properly work as input in the display function
            row_1_antepenultimate = mean_error_row_Combined.iloc[0]  # get first row
            row_2_penultimate = mode_error_row_Combined.iloc[0]  # get second row
            row_3_last = last_error_row_Combined.iloc[0]  # get third row
            # Call function for displaying results with a search range
            outputResults_DSv1.display_DSV1_results_searchRange(frameResults, row_1_antepenultimate, row_2_penultimate, row_3_last)
                        #The next code until the next option is the code for creating an ouput file (csv)
            # Define the format for numeric columns
            qty_decimals = '{:.4f}'  # Choosed the number of four decimal places
            # Apply formatting to specific numeric columns
            floating_columns = ['Estimated Delay', 'delta min', 'delta max', 'uncertainty']
            DSv1CF_trend_SearchRange[floating_columns] = DSv1CF_trend_SearchRange[floating_columns].applymap(lambda x: qty_decimals.format(x))
            DSv1CF_cycle_SearchRange[floating_columns] = DSv1CF_cycle_SearchRange[floating_columns].applymap(lambda x: qty_decimals.format(x))
            mean_error_row_Combined[floating_columns] = mean_error_row_Combined[floating_columns].applymap(lambda x: qty_decimals.format(x))
            mode_error_row_Combined[floating_columns] = mode_error_row_Combined[floating_columns].applymap(lambda x: qty_decimals.format(x))
            last_error_row_Combined[floating_columns] = last_error_row_Combined[floating_columns].applymap(lambda x: qty_decimals.format(x))
            # first concatenation of the dataframes
            combined_df_A = pd.concat([DSv1CF_trend_SearchRange, header1, DSv1CF_cycle_SearchRange, header1], ignore_index=True)
            # concatanate the last four rows of the file
            combined_df_B = mean_error_row_Combined.append([mode_error_row_Combined, last_error_row_Combined], ignore_index=True)
            # second concatenation
            combined_df_CF_SR = pd.concat([combined_df_A, combined_df_B], ignore_index=True)
            banderaKnownDelay = 0
            # convert the dataframes concateneted to an output file in csv
            # combined_df_C.to_csv("resultsDSv1_CF_cycle_trend_SearchRange.csv", header=True, index=True)

    elif preprocessing_selectionAA == "Raw Data" and delayMethod_selectionAA == "Dispersion Spectra":
        prep_technique = "Raw Data"
        df_lcA_raw, df_lcB_raw = rawData_function.raw_data(dfA, dfB, hint_delay)
        filteredRawData = dispersionSpectraV1_Function.calculate_delay(df_lcA_raw, df_lcB_raw, hint_delay, prep_technique)
        # Option if the delay is known
        if banderaKnownDelay == 1:
            #filteredRawData.to_csv("resultsDSv1_RawData_KnownDelay.csv", index=True, header=True)
            # Get the last fourth rows of the DataFrame
            last_fourth_rows = filteredRawData.iloc[-4:]

            row_one_preantepenultimate = last_fourth_rows.iloc[0]  # get first row
            row_two_antepenultimate = last_fourth_rows.iloc[1]  # get second row
            row_three_penultimate = last_fourth_rows.iloc[2]  # get third row
            row_four_last = last_fourth_rows.iloc[3]  # get fourth row
            ##call fucntion to display the results
            outputResults_DSv1.display_DSV1_results_knownDelay(frameResults, row_one_preantepenultimate, row_two_antepenultimate, row_three_penultimate, row_four_last)
            banderaSearchRange = 0
         #Option with unkown time delay
        elif banderaSearchRange == 1:
            DSv1RawData_SearchRange = filteredRawData
            DSv1RawData_SearchRange.columns = ['Estimated Delay', 'delta min', 'delta max', 'search range', 'error',
                                               'prep_technique', 'uncertainty']
            DSv1RawData_SearchRange.drop('error', axis=1, inplace=True)
            DSv1RawData_SearchRange.drop(DSv1RawData_SearchRange.index[-4], axis=0, inplace=True)
            # Insert search range
            DSv1RawData_SearchRange['search range'] = DSv1RawData_SearchRange['search range'].apply(
                lambda x: str(input_valueCombobox))
            #DSv1RawData_SearchRange.to_csv("resultsDSv1_RawData_SearchRange.csv", index=True, header=True)
            # prepare the output
            last_three_rows = DSv1RawData_SearchRange.iloc[-3:]
            row_1_antepenultimate = last_three_rows.iloc[0]  # get first row
            row_2_penultimate = last_three_rows.iloc[1]  # get second row
            row_3_last = last_three_rows.iloc[2]  # get third row
            # Call function to display the results
            outputResults_DSv1.display_DSV1_results_searchRange(frameResults, row_1_antepenultimate, row_2_penultimate, row_3_last)
            banderaKnownDelay = 0
          ###################END of option##################
    elif preprocessing_selectionAA == 'Data Differencing' and delayMethod_selectionAA == 'Dispersion Spectra':
        prep_technique = "Differencing"
        df_lcA_diff, df_lcB_diff = data_differencing_function.data_differencing(dfA, dfB, hint_delay)
        filteredDiffData = dispersionSpectraV1_Function.calculate_delay(df_lcA_diff, df_lcB_diff, hint_delay, prep_technique)

        if banderaKnownDelay == 1:
            #filteredDiffData.to_csv("resultsDSv1_Differencing_KnownDelay.csv", index=True, header=True)
            # Get the last fourth rows of the DataFrame
            last_fourth_rows = filteredDiffData.iloc[-4:]

            row_one_preantepenultimate = last_fourth_rows.iloc[0]  # get first row
            row_two_antepenultimate = last_fourth_rows.iloc[1]  # get second row
            row_three_penultimate = last_fourth_rows.iloc[2]  # get third row
            row_four_last = last_fourth_rows.iloc[3]  # get fourth row
            ##call fucntion to display the results
            outputResults_DSv1.display_DSV1_results_knownDelay(frameResults, row_one_preantepenultimate, row_two_antepenultimate, row_three_penultimate, row_four_last)
             #Option with unkown time delay
        elif banderaSearchRange == 1:
            DSv1DiffData_SearchRange = filteredDiffData
            DSv1DiffData_SearchRange.columns = ['Estimated Delay', 'delta min', 'delta max', 'search range', 'error',
                                                'prep_technique', 'uncertainty']
            DSv1DiffData_SearchRange.drop('error', axis=1, inplace=True)
            DSv1DiffData_SearchRange.drop(DSv1DiffData_SearchRange.index[-4], axis=0, inplace=True)
            # Insert search range
            DSv1DiffData_SearchRange['search range'] = DSv1DiffData_SearchRange['search range'].apply(lambda x: str(input_valueCombobox))
            #DSv1DiffData_SearchRange.to_csv("resultsDSv1_Differencing_SearchRange.csv", index=True, header=True)
            # prepare the output
            last_three_rows = DSv1DiffData_SearchRange.iloc[-3:]
            row_1_antepenultimate = last_three_rows.iloc[0]  # get first row
            row_2_penultimate = last_three_rows.iloc[1]  # get second row
            row_3_last = last_three_rows.iloc[2]  # get third row
            # Call function to display the results
            outputResults_DSv1.display_DSV1_results_searchRange(frameResults, row_1_antepenultimate, row_2_penultimate, row_3_last)
           #End of option
    elif preprocessing_selectionAA == 'Simple Net Return' and delayMethod_selectionAA == 'Dispersion Spectra':
        prep_technique = "SimpleNetReturn"
        df_lcA_snr, df_lcB_snr = simpleNetReturn_function.simple_net_return(dfA, dfB, hint_delay)
        filteredSNR_Data = dispersionSpectraV1_Function.calculate_delay(df_lcA_snr, df_lcB_snr, hint_delay, prep_technique)
        if banderaKnownDelay == 1:
            #filteredSNR_Data.to_csv("resultsDSv1_SimpleNetReturn_KnownDelay.csv", index=True, header=True)
            # Get the last fourth rows of the DataFrame
            last_fourth_rows = filteredSNR_Data.iloc[-4:]
            row_one_preantepenultimate = last_fourth_rows.iloc[0]  # get first row
            row_two_antepenultimate = last_fourth_rows.iloc[1]  # get second row
            row_three_penultimate = last_fourth_rows.iloc[2]  # get third row
            row_four_last = last_fourth_rows.iloc[3]  # get fourth row
            # Call function for display results
            outputResults_DSv1.display_DSV1_results_knownDelay(frameResults, row_one_preantepenultimate, row_two_antepenultimate, row_three_penultimate, row_four_last)
            banderaSearchRange = 0
            #Option with unkown time delay
        elif banderaSearchRange == 1:
            DSv1SNR_Data_SearchRange = filteredSNR_Data
            DSv1SNR_Data_SearchRange.columns = ['Estimated Delay', 'delta min', 'delta max', 'search range', 'error',
                                                'prep_technique', 'uncertainty']
            DSv1SNR_Data_SearchRange.drop('error', axis=1, inplace=True)
            DSv1SNR_Data_SearchRange.drop(DSv1SNR_Data_SearchRange.index[-4], axis=0, inplace=True)
            # Insert search range
            DSv1SNR_Data_SearchRange['search range'] = DSv1SNR_Data_SearchRange['search range'].apply(lambda x: str(input_valueCombobox))
            #DSv1SNR_Data_SearchRange.to_csv("resultsDSv1_SimpleNetReturn_SearchRange.csv", index=True, header=True)
            # prepare the output
            last_three_rows = DSv1SNR_Data_SearchRange.iloc[-3:]
            row_1_antepenultimate = last_three_rows.iloc[0]  # get first row
            row_2_penultimate = last_three_rows.iloc[1]  # get second row
            row_3_last = last_three_rows.iloc[2]  # get third row
            # Call function to display the results
            outputResults_DSv1.display_DSV1_results_searchRange(frameResults, row_1_antepenultimate, row_2_penultimate, row_3_last)
            banderaKnownDelay = 0
          #End of option
    elif preprocessing_selectionAA == 'Wavelet Denoise lvl 1' and delayMethod_selectionAA == 'Dispersion Spectra':
        prep_technique = 'WaveletDenoise_lvl1'
        level = 1
        df_lcA_wd, df_lcB_wd = waveletDenoise_function.waveletDenoise(dfA, dfB, hint_delay, level)
        filteredWD_Data = dispersionSpectraV1_Function.calculate_delay(df_lcA_wd, df_lcB_wd, hint_delay, prep_technique)

        if banderaKnownDelay == 1:
            #filteredWD_Data.to_csv("resultsDSv1_WDlvl1_KnownDelay.csv", index=True, header=True)
            # Get the last fourth rows of the DataFrame
            last_fourth_rows = filteredWD_Data.iloc[-4:]

            row_one_preantepenultimate = last_fourth_rows.iloc[0]  # get first row
            row_two_antepenultimate = last_fourth_rows.iloc[1]  # get second row
            row_three_penultimate = last_fourth_rows.iloc[2]  # get third row
            row_four_last = last_fourth_rows.iloc[3]  # get fourth row
            # Call function for display results
            outputResults_DSv1.display_DSV1_results_knownDelay(frameResults, row_one_preantepenultimate, row_two_antepenultimate, row_three_penultimate, row_four_last)
            banderaSearchRange = 0
             #Option with unkown time delay
        elif banderaSearchRange == 1:
            DSv1WD_Data_SearchRange = filteredWD_Data
            DSv1WD_Data_SearchRange.columns = ['Estimated Delay', 'delta min', 'delta max', 'search range', 'error',
                                               'prep_technique', 'uncertainty']
            DSv1WD_Data_SearchRange.drop('error', axis=1, inplace=True)
            DSv1WD_Data_SearchRange.drop(DSv1WD_Data_SearchRange.index[-4], axis=0, inplace=True)
            # Insert search range
            DSv1WD_Data_SearchRange['search range'] = DSv1WD_Data_SearchRange['search range'].apply(lambda x: str(input_valueCombobox))
            #DSv1WD_Data_SearchRange.to_csv("resultsDSv1_WDlvl1_SearchRange.csv", index=True, header=True)
            # prepare the output
            last_three_rows = DSv1WD_Data_SearchRange.iloc[-3:]
            row_1_antepenultimate = last_three_rows.iloc[0]  # get first row
            row_2_penultimate = last_three_rows.iloc[1]  # get second row
            row_3_last = last_three_rows.iloc[2]  # get third row
            # Call function to display the results
            outputResults_DSv1.display_DSV1_results_searchRange(frameResults, row_1_antepenultimate, row_2_penultimate, row_3_last)
            banderaKnownDelay = 0
          #End of option
    # Wavelet denoise with a higher level that means a smoother time series
    elif preprocessing_selectionAA == 'Wavelet Denoise lvl 2' and delayMethod_selectionAA == 'Dispersion Spectra':
        prep_technique = 'WaveletDenoise_lvl2'
        level = 2
        df_lcA_wd, df_lcB_wd = waveletDenoise_function.waveletDenoise(dfA, dfB, hint_delay, level)
        filteredWD2_Data = dispersionSpectraV1_Function.calculate_delay(df_lcA_wd, df_lcB_wd, hint_delay, prep_technique)

        if banderaKnownDelay == 1:
            #filteredWD2_Data.to_csv("resultsDSv1_WDlvl2_KnownDelay.csv", index=True, header=True)
            # Get the last fourth rows of the DataFrame
            last_fourth_rows = filteredWD2_Data.iloc[-4:]

            row_one_preantepenultimate = last_fourth_rows.iloc[0]  # get first row
            row_two_antepenultimate = last_fourth_rows.iloc[1]  # get second row
            row_three_penultimate = last_fourth_rows.iloc[2]  # get third row
            row_four_last = last_fourth_rows.iloc[3]  # get fourth row
                        # Call function for display results
            outputResults_DSv1.display_DSV1_results_knownDelay(frameResults, row_one_preantepenultimate, row_two_antepenultimate, row_three_penultimate, row_four_last)
            banderaSearchRange = 0
        # Option with search by range
        elif banderaSearchRange == 1:
            DSv1WD2_Data_SearchRange = filteredWD2_Data
            DSv1WD2_Data_SearchRange.columns = ['Estimated Delay', 'delta min', 'delta max', 'search range', 'error',
                                                'prep_technique', 'uncertainty']
            DSv1WD2_Data_SearchRange.drop('error', axis=1, inplace=True)
            DSv1WD2_Data_SearchRange.drop(DSv1WD2_Data_SearchRange.index[-4], axis=0, inplace=True)
            # Insert search range
            DSv1WD2_Data_SearchRange['search range'] = DSv1WD2_Data_SearchRange['search range'].apply(
                lambda x: str(input_valueCombobox))
            #DSv1WD2_Data_SearchRange.to_csv("resultsDSv1_WDlvl2_SearchRange.csv", index=True, header=True)
            # prepare the output
            last_three_rows = DSv1WD2_Data_SearchRange.iloc[-3:]
            row_1_antepenultimate = last_three_rows.iloc[0]  # get first row
            row_2_penultimate = last_three_rows.iloc[1]  # get second row
            row_3_last = last_three_rows.iloc[2]  # get third row
                        # Call function to display the results
            outputResults_DSv1.display_DSV1_results_searchRange(frameResults, row_1_antepenultimate, row_2_penultimate, row_3_last)
            banderaKnownDelay = 0
    # Option DS with WD level 3
    elif preprocessing_selectionAA == 'Wavelet Denoise lvl 3' and delayMethod_selectionAA == 'Dispersion Spectra':
        prep_technique = 'WaveletDenoise_lvl3'
        level = 3
        df_lcA_wd, df_lcB_wd = waveletDenoise_function.waveletDenoise(dfA, dfB, hint_delay, level)
        filteredWD3_Data = dispersionSpectraV1_Function.calculate_delay(df_lcA_wd, df_lcB_wd, hint_delay, prep_technique)

        if banderaKnownDelay == 1:
            #filteredWD3_Data.to_csv("resultsDSv1_WDlvl3_KnownDelay.csv", index=True, header=True)
            # Get the last fourth rows of the DataFrame
            last_fourth_rows = filteredWD3_Data.iloc[-4:]

            row_one_preantepenultimate = last_fourth_rows.iloc[0]  # get first row
            row_two_antepenultimate = last_fourth_rows.iloc[1]  # get second row
            row_three_penultimate = last_fourth_rows.iloc[2]  # get third row
            row_four_last = last_fourth_rows.iloc[3]  # get fourth row
            # Call function to display results
            outputResults_DSv1.display_DSV1_results_knownDelay(frameResults, row_one_preantepenultimate, row_two_antepenultimate, row_three_penultimate, row_four_last)
            banderaSearchRange = 0
        # Option with search range WD 3
        elif banderaSearchRange == 1:
            DSv1WD3_Data_SearchRange = filteredWD3_Data
            DSv1WD3_Data_SearchRange.columns = ['Estimated Delay', 'delta min', 'delta max', 'search range', 'error',
                                                'prep_technique', 'uncertainty']
            DSv1WD3_Data_SearchRange.drop('error', axis=1, inplace=True)
            DSv1WD3_Data_SearchRange.drop(DSv1WD3_Data_SearchRange.index[-4], axis=0, inplace=True)
            # Insert search range
            DSv1WD3_Data_SearchRange['search range'] = DSv1WD3_Data_SearchRange['search range'].apply(
                lambda x: str(input_valueCombobox))
            #DSv1WD3_Data_SearchRange.to_csv("resultsDSv1_WDlvl3_SearchRange.csv", index=True, header=True)
            # prepare the output
            last_three_rows = DSv1WD3_Data_SearchRange.iloc[-3:]
            row_1_antepenultimate = last_three_rows.iloc[0]  # get first row
            row_2_penultimate = last_three_rows.iloc[1]  # get second row
            row_3_last = last_three_rows.iloc[2]  # get third row
            # Call function to display the results
            outputResults_DSv1.display_DSV1_results_searchRange(frameResults, row_1_antepenultimate, row_2_penultimate, row_3_last)
            banderaKnownDelay = 0

    elif preprocessing_selectionAA == 'Raw Data' and delayMethod_selectionAA == 'Locally Normalized DCF':
        # Set the preprocessing technique
        prep_technique = "Raw Data"
        # Call function to obtain the raw data in a standarized form
        df_lcA_raw, df_lcB_raw = rawData_function.raw_data(dfA, dfB, hint_delay)
        # Call function to obtain the estimated delay through the LNDCF algorithm
        LNDCF_RawData_KD = function_lndcf.find_lndcf_delay(df_lcA_raw, df_lcB_raw, hint_delay, prep_technique)
        # Ensure that results obtained are in numeric form
        LNDCF_RawData_KD['LNDCF_Max'] = pd.to_numeric(LNDCF_RawData_KD['LNDCF_Max'], errors='coerce')
        LNDCF_RawData_KD['LNDCFERR'] = pd.to_numeric(LNDCF_RawData_KD['LNDCFERR'], errors='coerce')
        LNDCF_RawData_KD['EstimatedDelay'] = pd.to_numeric(LNDCF_RawData_KD['EstimatedDelay'], errors='coerce')
        LNDCF_RawData_KD['bin'] = pd.to_numeric(LNDCF_RawData_KD['bin'], errors='coerce')
        LNDCF_RawData_KD['delta min'] = pd.to_numeric(LNDCF_RawData_KD['delta min'], errors='coerce')
        LNDCF_RawData_KD['delta max'] = pd.to_numeric(LNDCF_RawData_KD['delta max'], errors='coerce')
        LNDCF_RawData_KD['uncertainty'] = pd.to_numeric(LNDCF_RawData_KD['uncertainty'], errors='coerce')
        LNDCF_RawData_KD['error'] = pd.to_numeric(LNDCF_RawData_KD['error'], errors='coerce')

        if banderaKnownDelay == 1:
            #LNDCF_RawData.to_csv("resultsLNDCF_RawData_KnownDelay.csv", index=True, header=True)
            last_four_rows = LNDCF_RawData_KD.iloc[-4:]

            row1_preantepenultimate = last_four_rows.iloc[0]  # get first row
            row2_antepenultimate = last_four_rows.iloc[1]  # get second row
            row3_penultimate = last_four_rows.iloc[2]  # get third row
            row4_last = last_four_rows.iloc[3]  # get fourth row
            # Call function to display the output results in a treeview
            outputResults_LNDCF.display_lndcf_results_knownDelay(frameResults, row1_preantepenultimate, row2_antepenultimate, row3_penultimate, row4_last)
            banderaSearchRange = 0
        elif banderaSearchRange == 1:
            LNDCF_RawData_SR = LNDCF_RawData_KD.copy()
            LNDCF_RawData_SR.columns = ['LNDCF_Max', 'LNDCF_Err', 'Estimated Delay', 'bin', 'delta min', 'delta max',
                                     'search range', 'prep_technique', 'error', 'uncertainty']
            LNDCF_RawData_SR.drop('error', axis=1, inplace=True)
            LNDCF_RawData_SR.drop(LNDCF_RawData_SR.index[-4], axis=0, inplace=True)
            # Insert search range
            LNDCF_RawData_SR['search range'] = LNDCF_RawData_SR['search range'].apply(lambda x: str(input_valueCombobox))
            #LNDCF_RawData.to_csv("resultsLNDCF_RawData_SearchRange.csv", index=True, header=True)
            # prepare the output
            last_three_rows = LNDCF_RawData_SR.iloc[-3:]
            row_1_antepenultimate = last_three_rows.iloc[0]  # get first row
            row_2_penultimate = last_three_rows.iloc[1]  # get second row
            row_3_last = last_three_rows.iloc[2]  # get third row
            # Call function to display the output results in a treeview by a search range
            outputResults_LNDCF.display_lndcf_results_searchRange(frameResults, row_1_antepenultimate, row_2_penultimate, row_3_last)
            banderaKnownDelay = 0

    elif preprocessing_selectionAA == 'Data Differencing' and delayMethod_selectionAA == 'Locally Normalized DCF':
        prep_technique = "Differencing"

        if banderaKnownDelay == 1:
            df_lcA_diff, df_lcB_diff = data_differencing_function.data_differencing(dfA, dfB, hint_delay)

            LNDCF_DiffData = function_lndcf.find_lndcf_delay(df_lcA_diff, df_lcB_diff, hint_delay, prep_technique)
            #
            LNDCF_DiffData['LNDCF_Max'] = pd.to_numeric(LNDCF_DiffData['LNDCF_Max'], errors='coerce')
            LNDCF_DiffData['LNDCFERR'] = pd.to_numeric(LNDCF_DiffData['LNDCFERR'], errors='coerce')
            LNDCF_DiffData['EstimatedDelay'] = pd.to_numeric(LNDCF_DiffData['EstimatedDelay'], errors='coerce')
            LNDCF_DiffData['bin'] = pd.to_numeric(LNDCF_DiffData['bin'], errors='coerce')
            LNDCF_DiffData['delta min'] = pd.to_numeric(LNDCF_DiffData['delta min'], errors='coerce')
            LNDCF_DiffData['delta max'] = pd.to_numeric(LNDCF_DiffData['delta max'], errors='coerce')
            LNDCF_DiffData['uncertainty'] = pd.to_numeric(LNDCF_DiffData['uncertainty'], errors='coerce')
            LNDCF_DiffData['error'] = pd.to_numeric(LNDCF_DiffData['error'], errors='coerce')
            #LNDCF_DiffData.to_csv("resultsLNDCF_" + prep_technique + "_KnownDelay.csv", index=True, header=True)
            last_four_rows = LNDCF_DiffData.iloc[-4:]
            row1_preantepenultimate = last_four_rows.iloc[0]  # get first row
            row2_antepenultimate = last_four_rows.iloc[1]  # get second row
            row3_penultimate = last_four_rows.iloc[2]  # get third row
            row4_last = last_four_rows.iloc[3]  # get fourth row
            # Call function to display the output results in a treeview
            outputResults_LNDCF.display_lndcf_results_knownDelay(frameResults, row1_preantepenultimate, row2_antepenultimate, row3_penultimate, row4_last)
            banderaSearchRange = 0

        elif banderaSearchRange == 1:
            df_lcA_diff_sr, df_lcB_diff_sr = data_differencing_function.data_differencing(dfA, dfB, hint_delay)

            LNDCF_DiffData_SR = function_lndcf.find_lndcf_delay(df_lcA_diff_sr, df_lcB_diff_sr, hint_delay, prep_technique)
            #
            LNDCF_DiffData_SR['LNDCF_Max'] = pd.to_numeric(LNDCF_DiffData_SR['LNDCF_Max'], errors='coerce')
            LNDCF_DiffData_SR['LNDCFERR'] = pd.to_numeric(LNDCF_DiffData_SR['LNDCFERR'], errors='coerce')
            LNDCF_DiffData_SR['EstimatedDelay'] = pd.to_numeric(LNDCF_DiffData_SR['EstimatedDelay'], errors='coerce')
            LNDCF_DiffData_SR['bin'] = pd.to_numeric(LNDCF_DiffData_SR['bin'], errors='coerce')
            LNDCF_DiffData_SR['delta min'] = pd.to_numeric(LNDCF_DiffData_SR['delta min'], errors='coerce')
            LNDCF_DiffData_SR['delta max'] = pd.to_numeric(LNDCF_DiffData_SR['delta max'], errors='coerce')
            LNDCF_DiffData_SR['uncertainty'] = pd.to_numeric(LNDCF_DiffData_SR['uncertainty'], errors='coerce')
            LNDCF_DiffData_SR['error'] = pd.to_numeric(LNDCF_DiffData_SR['error'], errors='coerce')

            LNDCF_DiffData_SR.columns = ['LNDCF_Max', 'LNDCF_Err', 'Estimated Delay', 'bin', 'delta min', 'delta max',
                                         'search range', 'prep_technique', 'error', 'uncertainty']
            LNDCF_DiffData_SR.drop('error', axis=1, inplace=True)
            LNDCF_DiffData_SR.drop(LNDCF_DiffData_SR.index[-4], axis=0, inplace=True)
            # Insert search range
            LNDCF_DiffData_SR['search range'] = LNDCF_DiffData_SR['search range'].apply(lambda x: str(input_valueCombobox))
            #LNDCF_DiffData_SR.to_csv("resultsLNDCF_" + prep_technique + "_SearchRange.csv", index=True, header=True)
            # prepare LNDCF_DiffData_SR output
            last_three_rows = LNDCF_DiffData_SR.iloc[-3:]
            row_1_antepenultimate = last_three_rows.iloc[0]  # get first row
            row_2_penultimate = last_three_rows.iloc[1]  # get second row
            row_3_last = last_three_rows.iloc[2]  # get third row
            # Call function for displaying results with a search range
            outputResults_LNDCF.display_lndcf_results_searchRange(frameResults, row_1_antepenultimate, row_2_penultimate, row_3_last)
            banderaKnownDelay = 0

    elif preprocessing_selectionAA == 'Simple Net Return' and delayMethod_selectionAA == 'Locally Normalized DCF':
        prep_technique = "SimpleNetReturn"

        if banderaKnownDelay == 1:

            df_lcA_snr, df_lcB_snr = simpleNetReturn_function.simple_net_return(dfA, dfB, hint_delay)

            LNDCF_SNR_Data = function_lndcf.find_lndcf_delay(df_lcA_snr, df_lcB_snr, hint_delay, prep_technique)
            #
            LNDCF_SNR_Data['LNDCF_Max'] = pd.to_numeric(LNDCF_SNR_Data['LNDCF_Max'], errors='coerce')
            LNDCF_SNR_Data['LNDCFERR'] = pd.to_numeric(LNDCF_SNR_Data['LNDCFERR'], errors='coerce')
            LNDCF_SNR_Data['EstimatedDelay'] = pd.to_numeric(LNDCF_SNR_Data['EstimatedDelay'], errors='coerce')
            LNDCF_SNR_Data['bin'] = pd.to_numeric(LNDCF_SNR_Data['bin'], errors='coerce')
            LNDCF_SNR_Data['delta min'] = pd.to_numeric(LNDCF_SNR_Data['delta min'], errors='coerce')
            LNDCF_SNR_Data['delta max'] = pd.to_numeric(LNDCF_SNR_Data['delta max'], errors='coerce')
            LNDCF_SNR_Data['uncertainty'] = pd.to_numeric(LNDCF_SNR_Data['uncertainty'], errors='coerce')
            LNDCF_SNR_Data['error'] = pd.to_numeric(LNDCF_SNR_Data['error'], errors='coerce')
            #LNDCF_SNR_Data.to_csv("resultsLNDCF_SimpleNetReturn_KnownDelay.csv", index=True, header=True)
            last_four_rows = LNDCF_SNR_Data.iloc[-4:]

            row1_preantepenultimate = last_four_rows.iloc[0]  # get first row
            row2_antepenultimate = last_four_rows.iloc[1]  # get second row
            row3_penultimate = last_four_rows.iloc[2]  # get third row
            row4_last = last_four_rows.iloc[3]  # get fourth row
                        # Call function to display the output results in a treeview
            outputResults_LNDCF.display_lndcf_results_knownDelay(frameResults, row1_preantepenultimate, row2_antepenultimate, row3_penultimate, row4_last)
            banderaSearchRange = 0

        elif banderaSearchRange == 1:
            df_lcA_snr, df_lcB_snr = simpleNetReturn_function.simple_net_return(dfA, dfB, hint_delay)

            LNDCF_SNR_Data_SR = function_lndcf.find_lndcf_delay(df_lcA_snr, df_lcB_snr, hint_delay, prep_technique)
            #
            LNDCF_SNR_Data_SR['LNDCF_Max'] = pd.to_numeric(LNDCF_SNR_Data_SR['LNDCF_Max'], errors='coerce')
            LNDCF_SNR_Data_SR['LNDCFERR'] = pd.to_numeric(LNDCF_SNR_Data_SR['LNDCFERR'], errors='coerce')
            LNDCF_SNR_Data_SR['EstimatedDelay'] = pd.to_numeric(LNDCF_SNR_Data_SR['EstimatedDelay'], errors='coerce')
            LNDCF_SNR_Data_SR['bin'] = pd.to_numeric(LNDCF_SNR_Data_SR['bin'], errors='coerce')
            LNDCF_SNR_Data_SR['delta min'] = pd.to_numeric(LNDCF_SNR_Data_SR['delta min'], errors='coerce')
            LNDCF_SNR_Data_SR['delta max'] = pd.to_numeric(LNDCF_SNR_Data_SR['delta max'], errors='coerce')
            LNDCF_SNR_Data_SR['uncertainty'] = pd.to_numeric(LNDCF_SNR_Data_SR['uncertainty'], errors='coerce')
            LNDCF_SNR_Data_SR['error'] = pd.to_numeric(LNDCF_SNR_Data_SR['error'], errors='coerce')

            LNDCF_SNR_Data_SR.columns = ['LNDCF_Max', 'LNDCF_Err', 'Estimated Delay', 'bin', 'delta min', 'delta max',
                                         'search range', 'prep_technique', 'error', 'uncertainty']
            LNDCF_SNR_Data_SR.drop('error', axis=1, inplace=True)
            LNDCF_SNR_Data_SR.drop(LNDCF_SNR_Data_SR.index[-4], axis=0, inplace=True)
            # Insert search range
            LNDCF_SNR_Data_SR['search range'] = LNDCF_SNR_Data_SR['search range'].apply(lambda x: str(input_valueCombobox))
            LNDCF_SNR_Data_SR.to_csv("resultsLNDCF_SimpleNetReturn_SearchRange.csv", index=True, header=True)
            # prepare LNDCF_SNR_Data_SR output
            last_three_rows = LNDCF_SNR_Data_SR.iloc[-3:]
            row_1_antepenultimate = last_three_rows.iloc[0]  # get first row
            row_2_penultimate = last_three_rows.iloc[1]  # get second row
            row_3_last = last_three_rows.iloc[2]  # get third row
                        # Call function for displaying results with a search range
            outputResults_LNDCF.display_lndcf_results_searchRange(frameResults, row_1_antepenultimate, row_2_penultimate, row_3_last)
            banderaKnownDelay = 0

    elif preprocessing_selectionAA == "Christiano-Fitzgerald filter" and delayMethod_selectionAA == "Locally Normalized DCF":
        prep_techniqueA = "CF-trend"
        prep_techniqueB = "CF-cycle"

        if banderaKnownDelay == 1:
            # obtain cycle and trend of CF filter
            dfCycle_lcA, dfCycle_lcB, dfTrend_lcA, dfTrend_lcB = CFfilter_function.cf_filter(dfA, dfB, hint_delay)

            LNDCF_CFcycle_Data = function_lndcf.find_lndcf_delay(dfCycle_lcA, dfCycle_lcB, hint_delay, prep_techniqueB)

            LNDCF_CFtrend_Data = function_lndcf.find_lndcf_delay(dfTrend_lcA, dfTrend_lcB, hint_delay, prep_techniqueA)
            #
            # Ensure that the following columns are numeric for format output
            LNDCF_CFtrend_Data['LNDCF_Max'] = pd.to_numeric(LNDCF_CFtrend_Data['LNDCF_Max'], errors='coerce')
            LNDCF_CFtrend_Data['LNDCFERR'] = pd.to_numeric(LNDCF_CFtrend_Data['LNDCFERR'], errors='coerce')
            LNDCF_CFtrend_Data['EstimatedDelay'] = pd.to_numeric(LNDCF_CFtrend_Data['EstimatedDelay'], errors='coerce')
            LNDCF_CFtrend_Data['bin'] = pd.to_numeric(LNDCF_CFtrend_Data['bin'], errors='coerce')
            LNDCF_CFtrend_Data['delta min'] = pd.to_numeric(LNDCF_CFtrend_Data['delta min'], errors='coerce')
            LNDCF_CFtrend_Data['delta max'] = pd.to_numeric(LNDCF_CFtrend_Data['delta max'], errors='coerce')
            LNDCF_CFtrend_Data['uncertainty'] = pd.to_numeric(LNDCF_CFtrend_Data['uncertainty'], errors='coerce')
            LNDCF_CFtrend_Data['error'] = pd.to_numeric(LNDCF_CFtrend_Data['error'], errors='coerce')
            # Ensure that the following columns are numeric for format output
            LNDCF_CFcycle_Data['LNDCF_Max'] = pd.to_numeric(LNDCF_CFcycle_Data['LNDCF_Max'], errors='coerce')
            LNDCF_CFcycle_Data['LNDCFERR'] = pd.to_numeric(LNDCF_CFcycle_Data['LNDCFERR'], errors='coerce')
            LNDCF_CFcycle_Data['EstimatedDelay'] = pd.to_numeric(LNDCF_CFcycle_Data['EstimatedDelay'], errors='coerce')
            LNDCF_CFcycle_Data['bin'] = pd.to_numeric(LNDCF_CFcycle_Data['bin'], errors='coerce')
            LNDCF_CFcycle_Data['delta min'] = pd.to_numeric(LNDCF_CFcycle_Data['delta min'], errors='coerce')
            LNDCF_CFcycle_Data['delta max'] = pd.to_numeric(LNDCF_CFcycle_Data['delta max'], errors='coerce')
            LNDCF_CFcycle_Data['uncertainty'] = pd.to_numeric(LNDCF_CFcycle_Data['uncertainty'], errors='coerce')
            LNDCF_CFcycle_Data['error'] = pd.to_numeric(LNDCF_CFcycle_Data['error'], errors='coerce')
            # obtain the last four rows from cycle
            last_fourth_cycle_rows = LNDCF_CFcycle_Data.iloc[-4:]
            row_one_min_cycle_preantepenultimate = last_fourth_cycle_rows.iloc[0]  # get first row
            row_two_max_cycle_antepenultimate = last_fourth_cycle_rows.iloc[1]  # get second row
            row_three_mean_cycle_penultimate = last_fourth_cycle_rows.iloc[2]  # get third row
            row_four_mode_cycle_last = last_fourth_cycle_rows.iloc[3]  # get fourth row
            # obtain the last four rows from trend
            last_fourth_trend_rows = LNDCF_CFtrend_Data.iloc[-4:]
            row_one_min_trend_preantepenultimate = last_fourth_trend_rows.iloc[0]  # get first row
            row_two_max_trend_antepenultimate = last_fourth_trend_rows.iloc[1]  # get second row
            row_three_mean_trend_penultimate = last_fourth_trend_rows.iloc[2]  # get third row
            row_four_mode_trend_last = last_fourth_trend_rows.iloc[3]  # get fourth row
            # Calculate the combined min error
            min_error_row_Combined = pd.DataFrame({
                'LNDCF_Max': (row_one_min_cycle_preantepenultimate["LNDCF_Max"] + row_one_min_trend_preantepenultimate["LNDCF_Max"]) / 2,
                'LNDCFERR': (row_one_min_cycle_preantepenultimate["LNDCFERR"] + row_one_min_trend_preantepenultimate["LNDCFERR"]) / 2,
                'EstimatedDelay': (row_one_min_cycle_preantepenultimate["EstimatedDelay"] +
                                   row_one_min_trend_preantepenultimate["EstimatedDelay"]) / 2,
                'bin': (row_one_min_cycle_preantepenultimate['bin'] + row_one_min_trend_preantepenultimate["bin"]) / 2,
                'delta min': (row_one_min_cycle_preantepenultimate['delta min'] + row_one_min_trend_preantepenultimate[
                    "delta min"]) / 2,
                'delta max': (row_one_min_cycle_preantepenultimate["delta max"] + row_one_min_trend_preantepenultimate[
                    "delta max"]) / 2,
                'True delay': row_one_min_cycle_preantepenultimate["True delay"],
                'prep_technique': row_one_min_cycle_preantepenultimate["prep_technique"],
                'uncertainty': (row_one_min_cycle_preantepenultimate['uncertainty'] +
                                row_one_min_trend_preantepenultimate['uncertainty']) / 2,
                'error': abs(((row_one_min_cycle_preantepenultimate["EstimatedDelay"] +
                               row_one_min_trend_preantepenultimate["EstimatedDelay"]) / 2) -
                          row_one_min_cycle_preantepenultimate["True delay"])}, index=[0])
            min_error_row_Combined.iloc[0, -3] = 'min trend/cycle'
            # Calculate the combined mean
            max_error_row_Combined = pd.DataFrame({
                'LNDCF_Max': (row_two_max_cycle_antepenultimate["LNDCF_Max"] + row_two_max_trend_antepenultimate["LNDCF_Max"]) / 2,
                'LNDCFERR': (row_two_max_cycle_antepenultimate["LNDCFERR"] + row_two_max_trend_antepenultimate["LNDCFERR"]) / 2,
                'EstimatedDelay': (row_two_max_cycle_antepenultimate["EstimatedDelay"] +
                                   row_two_max_trend_antepenultimate["EstimatedDelay"]) / 2,
                'bin': (row_two_max_cycle_antepenultimate['bin'] + row_two_max_trend_antepenultimate["bin"]) / 2,
                'delta min': (row_two_max_cycle_antepenultimate['delta min'] + row_two_max_trend_antepenultimate["delta min"]) / 2,
                'delta max': (row_two_max_cycle_antepenultimate["delta max"] + row_two_max_trend_antepenultimate["delta max"]) / 2,
                'True delay': row_two_max_cycle_antepenultimate["True delay"],
                'prep_technique': row_two_max_cycle_antepenultimate["prep_technique"],
                'uncertainty': (row_two_max_cycle_antepenultimate['uncertainty'] + row_two_max_trend_antepenultimate['uncertainty']) / 2,
                'error': abs(((row_two_max_cycle_antepenultimate["EstimatedDelay"] + row_two_max_trend_antepenultimate[
                    "EstimatedDelay"]) / 2) - row_two_max_cycle_antepenultimate["True delay"])}, index=[0])
            max_error_row_Combined.iloc[0, -3] = 'max trend/cycle'
            # Calculate the combined mode
            mean_error_row_Combined = pd.DataFrame({
                'LNDCF_Max': (row_three_mean_cycle_penultimate["LNDCF_Max"] + row_three_mean_trend_penultimate["LNDCF_Max"]) / 2,
                'LNDCFERR': (row_three_mean_cycle_penultimate["LNDCFERR"] + row_three_mean_trend_penultimate["LNDCFERR"]) / 2,
                'EstimatedDelay': (row_three_mean_cycle_penultimate["EstimatedDelay"] +
                                   row_three_mean_trend_penultimate["EstimatedDelay"]) / 2,
                'bin': (row_three_mean_cycle_penultimate['bin'] + row_three_mean_trend_penultimate["bin"]) / 2,
                'delta min': (row_three_mean_cycle_penultimate['delta min'] + row_three_mean_trend_penultimate["delta min"]) / 2,
                'delta max': (row_three_mean_cycle_penultimate["delta max"] + row_three_mean_trend_penultimate["delta max"]) / 2,
                'True delay': row_three_mean_cycle_penultimate["True delay"],
                'prep_technique': row_three_mean_cycle_penultimate["prep_technique"],
                'uncertainty': (row_three_mean_cycle_penultimate['uncertainty'] + row_three_mean_trend_penultimate['uncertainty']) / 2,
                'error': abs(((row_three_mean_cycle_penultimate["EstimatedDelay"] + row_three_mean_trend_penultimate[
                    "EstimatedDelay"]) / 2) - row_three_mean_cycle_penultimate["True delay"])}, index=[0])
            mean_error_row_Combined.iloc[0, -3] = 'mean trend/cycle'
            # Calculate the average of the combined mean and mode
            last_mode_error_row_Combined = pd.DataFrame({
                'LNDCF_Max': (row_four_mode_cycle_last["LNDCF_Max"] + row_four_mode_trend_last["LNDCF_Max"]) / 2,
                'LNDCFERR': (row_four_mode_cycle_last["LNDCFERR"] + row_four_mode_trend_last["LNDCFERR"]) / 2,
                'EstimatedDelay': (row_four_mode_cycle_last["EstimatedDelay"] + row_four_mode_trend_last["EstimatedDelay"]) / 2,
                'bin': (row_four_mode_cycle_last['bin'] + row_four_mode_trend_last["bin"]) / 2,
                'delta min': (row_four_mode_cycle_last['delta min'] + row_four_mode_trend_last["delta min"]) / 2,
                'delta max': (row_four_mode_cycle_last["delta max"] + row_four_mode_trend_last["delta max"]) / 2,
                'True delay': row_four_mode_cycle_last["True delay"],
                'prep_technique': row_four_mode_cycle_last["prep_technique"],
                'uncertainty': (row_four_mode_cycle_last['uncertainty'] + row_four_mode_trend_last['uncertainty']) / 2,
                'error': abs(((row_four_mode_cycle_last["EstimatedDelay"] + row_four_mode_trend_last[
                    "EstimatedDelay"]) / 2) - row_four_mode_cycle_last["True delay"])}, index=[0])
            last_mode_error_row_Combined.iloc[0, -3] = 'mode trend/cycle'
            # Create a header to insert to the concatenated DataFrames
            header1 = pd.DataFrame([{'LNDCF_Max': 'LNDCF_Max', 'LNDCFERR': 'LNDCFERR', 'EstimatedDelay': 'EstimatedDelay', 'bin': 'bin',
                                     'delta min': 'delta min', 'delta max': 'delta max', 'True delay': 'True delay',
                                     'prep_technique': 'prep_technique', 'uncertainty': 'uncertainty', 'error': 'error'}])

            # Ensure that the following columns are numeric for format output
            min_error_row_Combined['LNDCF_Max'] = pd.to_numeric(min_error_row_Combined['LNDCF_Max'], errors='coerce')
            min_error_row_Combined['LNDCFERR'] = pd.to_numeric(min_error_row_Combined['LNDCFERR'], errors='coerce')
            min_error_row_Combined['EstimatedDelay'] = pd.to_numeric(min_error_row_Combined['EstimatedDelay'], errors='coerce')
            min_error_row_Combined['bin'] = pd.to_numeric(min_error_row_Combined['bin'], errors='coerce')
            min_error_row_Combined['delta min'] = pd.to_numeric(min_error_row_Combined['delta min'], errors='coerce')
            min_error_row_Combined['delta max'] = pd.to_numeric(min_error_row_Combined['delta max'], errors='coerce')
            min_error_row_Combined['uncertainty'] = pd.to_numeric(min_error_row_Combined['uncertainty'], errors='coerce')
            min_error_row_Combined['error'] = pd.to_numeric(min_error_row_Combined['error'], errors='coerce')
            # Ensure that the following columns are numeric for format output
            max_error_row_Combined['LNDCF_Max'] = pd.to_numeric(max_error_row_Combined['LNDCF_Max'], errors='coerce')
            max_error_row_Combined['LNDCFERR'] = pd.to_numeric(max_error_row_Combined['LNDCFERR'], errors='coerce')
            max_error_row_Combined['EstimatedDelay'] = pd.to_numeric(max_error_row_Combined['EstimatedDelay'], errors='coerce')
            max_error_row_Combined['bin'] = pd.to_numeric(max_error_row_Combined['bin'], errors='coerce')
            max_error_row_Combined['delta min'] = pd.to_numeric(max_error_row_Combined['delta min'], errors='coerce')
            max_error_row_Combined['delta max'] = pd.to_numeric(max_error_row_Combined['delta max'], errors='coerce')
            max_error_row_Combined['uncertainty'] = pd.to_numeric(max_error_row_Combined['uncertainty'],errors='coerce')
            max_error_row_Combined['error'] = pd.to_numeric(max_error_row_Combined['error'], errors='coerce')
            # Ensure that the following columns are numeric for format output
            mean_error_row_Combined['LNDCF_Max'] = pd.to_numeric(mean_error_row_Combined['LNDCF_Max'], errors='coerce')
            mean_error_row_Combined['LNDCFERR'] = pd.to_numeric(mean_error_row_Combined['LNDCFERR'], errors='coerce')
            mean_error_row_Combined['EstimatedDelay'] = pd.to_numeric(mean_error_row_Combined['EstimatedDelay'], errors='coerce')
            mean_error_row_Combined['bin'] = pd.to_numeric(mean_error_row_Combined['bin'], errors='coerce')
            mean_error_row_Combined['delta min'] = pd.to_numeric(mean_error_row_Combined['delta min'], errors='coerce')
            mean_error_row_Combined['delta max'] = pd.to_numeric(mean_error_row_Combined['delta max'], errors='coerce')
            mean_error_row_Combined['uncertainty'] = pd.to_numeric(mean_error_row_Combined['uncertainty'], errors='coerce')
            mean_error_row_Combined['error'] = pd.to_numeric(mean_error_row_Combined['error'], errors='coerce')
            # Ensure that the following columns are numeric for format output
            last_mode_error_row_Combined['LNDCF_Max'] = pd.to_numeric(last_mode_error_row_Combined['LNDCF_Max'], errors='coerce')
            last_mode_error_row_Combined['LNDCFERR'] = pd.to_numeric(last_mode_error_row_Combined['LNDCFERR'], errors='coerce')
            last_mode_error_row_Combined['EstimatedDelay'] = pd.to_numeric(last_mode_error_row_Combined['EstimatedDelay'], errors='coerce')
            last_mode_error_row_Combined['bin'] = pd.to_numeric(last_mode_error_row_Combined['bin'], errors='coerce')
            last_mode_error_row_Combined['delta min'] = pd.to_numeric(last_mode_error_row_Combined['delta min'], errors='coerce')
            last_mode_error_row_Combined['delta max'] = pd.to_numeric(last_mode_error_row_Combined['delta max'], errors='coerce')
            last_mode_error_row_Combined['uncertainty'] = pd.to_numeric(last_mode_error_row_Combined['uncertainty'], errors='coerce')
            last_mode_error_row_Combined['error'] = pd.to_numeric(last_mode_error_row_Combined['error'], errors='coerce')
            # Convert each DataFrame into a Series by selecting the first row
            min_error_preantepenultimate = min_error_row_Combined.iloc[0]
            max_error_antepenultimate = max_error_row_Combined.iloc[0]
            mean_error_penultimate = mean_error_row_Combined.iloc[0]
            last_mode_error_last = last_mode_error_row_Combined.iloc[0]
                                    # Call function to display the output results in a treeview
            outputResults_LNDCF.display_lndcf_results_knownDelay(frameResults, min_error_preantepenultimate, max_error_antepenultimate, mean_error_penultimate, last_mode_error_last)
            # The next piece of code is for creating the output file csv
            # Define the format for numeric columns
            qty_decimals = '{:.4f}'  # Choosed the number of four decimal places
            # Apply formatting to specific numeric columns
            floating_columns = ['LNDCF_Max', 'LNDCFERR', 'EstimatedDelay', 'bin', 'delta min', 'delta max', 'uncertainty', 'error']
            LNDCF_CFcycle_Data[floating_columns] = LNDCF_CFcycle_Data[floating_columns].applymap(lambda x: qty_decimals.format(x))
            LNDCF_CFtrend_Data[floating_columns] = LNDCF_CFtrend_Data[floating_columns].applymap(lambda x: qty_decimals.format(x))
            ##
            min_error_row_Combined[floating_columns] = min_error_row_Combined[floating_columns].applymap(lambda x: qty_decimals.format(x))
            max_error_row_Combined[floating_columns] = max_error_row_Combined[floating_columns].applymap(lambda x: qty_decimals.format(x))
            mean_error_row_Combined[floating_columns] = mean_error_row_Combined[floating_columns].applymap(lambda x: qty_decimals.format(x))
            last_mode_error_row_Combined[floating_columns] = last_mode_error_row_Combined[floating_columns].applymap(lambda x: qty_decimals.format(x))
            # first concataneion of the dataframes
            combined_df_A = pd.concat([LNDCF_CFtrend_Data, header1, LNDCF_CFcycle_Data, header1], ignore_index=True)
            # concatanate the last four rows of the file
            combined_df_B = min_error_row_Combined.append([max_error_row_Combined, mean_error_row_Combined, last_mode_error_row_Combined], ignore_index=True)
            # second concatenation
            combined_df_LNDCF_CF_KD = pd.concat([combined_df_A, combined_df_B], ignore_index=True)
            # convert the dataframes concateneted to an output file in csv
            #combined_df_C.to_csv("resultsLNDCF_CF_cycle_trend_KnownDelay.csv", header=True, index=True)
            banderaSearchRange = 0

        elif banderaSearchRange == 1:
            # obtain cycle and trend of CF filter
            dfCycle_lcA, dfCycle_lcB, dfTrend_lcA, dfTrend_lcB = CFfilter_function.cf_filter(dfA, dfB, hint_delay)

            LNDCF_CFcycle_Data = function_lndcf.find_lndcf_delay(dfCycle_lcA, dfCycle_lcB, hint_delay, prep_techniqueB)

            LNDCF_CFtrend_Data = function_lndcf.find_lndcf_delay(dfTrend_lcA, dfTrend_lcB, hint_delay, prep_techniqueA)
            #
            # Ensure that the following columns are numeric for format output
            LNDCF_CFtrend_Data['LNDCF_Max'] = pd.to_numeric(LNDCF_CFtrend_Data['LNDCF_Max'], errors='coerce')
            LNDCF_CFtrend_Data['LNDCFERR'] = pd.to_numeric(LNDCF_CFtrend_Data['LNDCFERR'], errors='coerce')
            LNDCF_CFtrend_Data['EstimatedDelay'] = pd.to_numeric(LNDCF_CFtrend_Data['EstimatedDelay'], errors='coerce')
            LNDCF_CFtrend_Data['bin'] = pd.to_numeric(LNDCF_CFtrend_Data['bin'], errors='coerce')
            LNDCF_CFtrend_Data['delta min'] = pd.to_numeric(LNDCF_CFtrend_Data['delta min'], errors='coerce')
            LNDCF_CFtrend_Data['delta max'] = pd.to_numeric(LNDCF_CFtrend_Data['delta max'], errors='coerce')
            LNDCF_CFtrend_Data['uncertainty'] = pd.to_numeric(LNDCF_CFtrend_Data['uncertainty'], errors='coerce')
            LNDCF_CFtrend_Data['error'] = pd.to_numeric(LNDCF_CFtrend_Data['error'], errors='coerce')
            # Ensure that the following columns are numeric for format output
            LNDCF_CFcycle_Data['LNDCF_Max'] = pd.to_numeric(LNDCF_CFcycle_Data['LNDCF_Max'], errors='coerce')
            LNDCF_CFcycle_Data['LNDCFERR'] = pd.to_numeric(LNDCF_CFcycle_Data['LNDCFERR'], errors='coerce')
            LNDCF_CFcycle_Data['EstimatedDelay'] = pd.to_numeric(LNDCF_CFcycle_Data['EstimatedDelay'], errors='coerce')
            LNDCF_CFcycle_Data['bin'] = pd.to_numeric(LNDCF_CFcycle_Data['bin'], errors='coerce')
            LNDCF_CFcycle_Data['delta min'] = pd.to_numeric(LNDCF_CFcycle_Data['delta min'], errors='coerce')
            LNDCF_CFcycle_Data['delta max'] = pd.to_numeric(LNDCF_CFcycle_Data['delta max'], errors='coerce')
            LNDCF_CFcycle_Data['uncertainty'] = pd.to_numeric(LNDCF_CFcycle_Data['uncertainty'], errors='coerce')
            LNDCF_CFcycle_Data['error'] = pd.to_numeric(LNDCF_CFcycle_Data['error'], errors='coerce')

            LNDCF_CFtrend_Data.columns = ['LNDCF_Max', 'LNDCF_Err', 'Estimated Delay', 'bin', 'delta min', 'delta max',
                                          'search range', 'prep_technique', 'uncertainty', 'error']
            LNDCF_CFcycle_Data.columns = ['LNDCF_Max', 'LNDCF_Err', 'Estimated Delay', 'bin', 'delta min', 'delta max',
                                          'search range', 'prep_technique', 'uncertainty', 'error']
            LNDCF_CFtrend_Data.drop('error', axis=1, inplace=True)
            LNDCF_CFtrend_Data.drop(LNDCF_CFtrend_Data.index[-4], axis=0, inplace=True)
            LNDCF_CFcycle_Data.drop('error', axis=1, inplace=True)
            LNDCF_CFcycle_Data.drop(LNDCF_CFcycle_Data.index[-4], axis=0, inplace=True)
            # Insert search range
            LNDCF_CFcycle_Data['search range'] = LNDCF_CFcycle_Data['search range'].apply(lambda x: str(input_valueCombobox))
            LNDCF_CFtrend_Data['search range'] = LNDCF_CFtrend_Data['search range'].apply(lambda x: str(input_valueCombobox))
            # obtain the last three rows from cycle
            last_three_cycle_rows = LNDCF_CFcycle_Data.iloc[-3:]
            row_one_max_cycle_antepenultimate = last_three_cycle_rows.iloc[0]  # get second row
            row_two_mean_cycle_penultimate = last_three_cycle_rows.iloc[1]  # get third row
            row_three_mode_cycle_last = last_three_cycle_rows.iloc[2]  # get fourth row
            # obtain the last four rows from trend
            last_three_trend_rows = LNDCF_CFtrend_Data.iloc[-3:]
            row_one_max_trend_antepenultimate = last_three_trend_rows.iloc[0]  # get second row
            row_two_mean_trend_penultimate = last_three_trend_rows.iloc[1]  # get third row
            row_three_mode_trend_last = last_three_trend_rows.iloc[2]  # get fourth row
            # Calculate the combined mean
            max_error_row_Combined = pd.DataFrame({
                'LNDCF_Max': (row_one_max_cycle_antepenultimate["LNDCF_Max"] + row_one_max_trend_antepenultimate[
                    "LNDCF_Max"]) / 2,
                'LNDCF_Err': (row_one_max_cycle_antepenultimate["LNDCF_Err"] + row_one_max_trend_antepenultimate[
                    "LNDCF_Err"]) / 2,
                'Estimated Delay': (row_one_max_cycle_antepenultimate["Estimated Delay"] +
                                    row_one_max_trend_antepenultimate["Estimated Delay"]) / 2,
                'bin': (row_one_max_cycle_antepenultimate['bin'] + row_one_max_trend_antepenultimate["bin"]) / 2,
                'delta min': (row_one_max_cycle_antepenultimate['delta min'] + row_one_max_trend_antepenultimate["delta min"]) / 2,
                'delta max': (row_one_max_cycle_antepenultimate["delta max"] + row_one_max_trend_antepenultimate["delta max"]) / 2,
                'search range': row_one_max_cycle_antepenultimate["search range"],
                'prep_technique': row_one_max_cycle_antepenultimate["prep_technique"],
                'uncertainty': (row_one_max_cycle_antepenultimate['uncertainty'] + row_one_max_trend_antepenultimate[
                    'uncertainty']) / 2}, index=[0])
            max_error_row_Combined.iloc[0, -2] = 'max trend/cycle'
            # Calculate the combined mode
            mean_error_row_Combined = pd.DataFrame({
                'LNDCF_Max': (row_two_mean_cycle_penultimate["LNDCF_Max"] + row_two_mean_trend_penultimate["LNDCF_Max"]) / 2,
                'LNDCF_Err': (row_two_mean_cycle_penultimate["LNDCF_Err"] + row_two_mean_trend_penultimate["LNDCF_Err"]) / 2,
                'Estimated Delay': (row_two_mean_cycle_penultimate["Estimated Delay"] + row_two_mean_trend_penultimate["Estimated Delay"]) / 2,
                'bin': (row_two_mean_cycle_penultimate['bin'] + row_two_mean_trend_penultimate["bin"]) / 2,
                'delta min': (row_two_mean_cycle_penultimate['delta min'] + row_two_mean_trend_penultimate["delta min"]) / 2,
                'delta max': (row_two_mean_cycle_penultimate["delta max"] + row_two_mean_trend_penultimate["delta max"]) / 2,
                'search range': row_two_mean_cycle_penultimate["search range"],
                'prep_technique': row_two_mean_cycle_penultimate["prep_technique"],
                'uncertainty': (row_two_mean_cycle_penultimate['uncertainty'] + row_two_mean_trend_penultimate['uncertainty']) / 2}, index=[0])
            mean_error_row_Combined.iloc[0, -2] = 'mean trend/cycle'
            # Calculate the average of the combined mean and mode
            last_error_mode_row_Combined = pd.DataFrame({
                'LNDCF_Max': (row_three_mode_cycle_last["LNDCF_Max"] + row_three_mode_trend_last["LNDCF_Max"]) / 2,
                'LNDCF_Err': (row_three_mode_cycle_last["LNDCF_Err"] + row_three_mode_trend_last["LNDCF_Err"]) / 2,
                'Estimated Delay': (row_three_mode_cycle_last["Estimated Delay"] + row_three_mode_trend_last[
                    "Estimated Delay"]) / 2,
                'bin': (row_three_mode_cycle_last['bin'] + row_three_mode_trend_last["bin"]) / 2,
                'delta min': (row_three_mode_cycle_last['delta min'] + row_three_mode_trend_last["delta min"]) / 2,
                'delta max': (row_three_mode_cycle_last["delta max"] + row_three_mode_trend_last["delta max"]) / 2,
                'search range': row_three_mode_cycle_last["search range"],
                'prep_technique': row_three_mode_cycle_last["prep_technique"],
                'uncertainty': (row_three_mode_cycle_last['uncertainty'] + row_three_mode_trend_last[
                    'uncertainty']) / 2}, index=[0])
            last_error_mode_row_Combined.iloc[0, -2] = 'mode trend/cycle'
            # Create a header to insert to the concatenated DataFrames
            header1 = pd.DataFrame([{'LNDCF_Max': 'LNDCF_Max', 'LNDCF_Err': 'LNDCF_Err',
                                     'Estimated Delay': 'Estimated Delay', 'bin': 'bin', 'delta min': 'delta min',
                                     'delta max': 'delta max', 'search range': 'search range',
                                     'prep_technique': 'prep_technique', 'uncertainty': 'uncertainty'}])
            # Ensure that the following columns are numeric for format output
            max_error_row_Combined['LNDCF_Max'] = pd.to_numeric(max_error_row_Combined['LNDCF_Max'], errors='coerce')
            max_error_row_Combined['LNDCF_Err'] = pd.to_numeric(max_error_row_Combined['LNDCF_Err'], errors='coerce')
            max_error_row_Combined['Estimated Delay'] = pd.to_numeric(max_error_row_Combined['Estimated Delay'], errors='coerce')
            max_error_row_Combined['bin'] = pd.to_numeric(max_error_row_Combined['bin'], errors='coerce')
            max_error_row_Combined['delta min'] = pd.to_numeric(max_error_row_Combined['delta min'], errors='coerce')
            max_error_row_Combined['delta max'] = pd.to_numeric(max_error_row_Combined['delta max'], errors='coerce')
            max_error_row_Combined['uncertainty'] = pd.to_numeric(max_error_row_Combined['uncertainty'], errors='coerce')
            # Ensure that the following columns are numeric for format output
            mean_error_row_Combined['LNDCF_Max'] = pd.to_numeric(mean_error_row_Combined['LNDCF_Max'], errors='coerce')
            mean_error_row_Combined['LNDCF_Err'] = pd.to_numeric(mean_error_row_Combined['LNDCF_Err'], errors='coerce')
            mean_error_row_Combined['Estimated Delay'] = pd.to_numeric(mean_error_row_Combined['Estimated Delay'], errors='coerce')
            mean_error_row_Combined['bin'] = pd.to_numeric(mean_error_row_Combined['bin'], errors='coerce')
            mean_error_row_Combined['delta min'] = pd.to_numeric(mean_error_row_Combined['delta min'], errors='coerce')
            mean_error_row_Combined['delta max'] = pd.to_numeric(mean_error_row_Combined['delta max'], errors='coerce')
            mean_error_row_Combined['uncertainty'] = pd.to_numeric(mean_error_row_Combined['uncertainty'], errors='coerce')
            # Ensure that the following columns are numeric for format output
            last_error_mode_row_Combined['LNDCF_Max'] = pd.to_numeric(last_error_mode_row_Combined['LNDCF_Max'], errors='coerce')
            last_error_mode_row_Combined['LNDCF_Err'] = pd.to_numeric(last_error_mode_row_Combined['LNDCF_Err'], errors='coerce')
            last_error_mode_row_Combined['Estimated Delay'] = pd.to_numeric(last_error_mode_row_Combined['Estimated Delay'], errors='coerce')
            last_error_mode_row_Combined['bin'] = pd.to_numeric(last_error_mode_row_Combined['bin'], errors='coerce')
            last_error_mode_row_Combined['delta min'] = pd.to_numeric(last_error_mode_row_Combined['delta min'], errors='coerce')
            last_error_mode_row_Combined['delta max'] = pd.to_numeric(last_error_mode_row_Combined['delta max'], errors='coerce')
            last_error_mode_row_Combined['uncertainty'] = pd.to_numeric(last_error_mode_row_Combined['uncertainty'], errors='coerce')
                        # Convert each DataFrame into a Series by selecting the first row
            max_error_antepenultimate = max_error_row_Combined.iloc[0]
            mean_error_penultimate = mean_error_row_Combined.iloc[0]
            last_error_mode_last = last_error_mode_row_Combined.iloc[0]
                                    # Call function for displaying results with a search range
            outputResults_LNDCF.display_lndcf_results_searchRange(frameResults, max_error_antepenultimate, mean_error_penultimate, last_error_mode_last)
            # The next code is for creating a csv file for output
            # Define the format for numeric columns
            qty_decimals = '{:.4f}'  # Choosed the number of four decimal places
            # Apply formatting to specific numeric columns
            floating_columns = ['LNDCF_Max', 'LNDCF_Err', 'Estimated Delay', 'bin', 'delta min', 'delta max', 'uncertainty']
            LNDCF_CFcycle_Data[floating_columns] = LNDCF_CFcycle_Data[floating_columns].applymap(lambda x: qty_decimals.format(x))
            LNDCF_CFtrend_Data[floating_columns] = LNDCF_CFtrend_Data[floating_columns].applymap(lambda x: qty_decimals.format(x))
            ##
            max_error_row_Combined[floating_columns] = max_error_row_Combined[floating_columns].applymap(lambda x: qty_decimals.format(x))
            mean_error_row_Combined[floating_columns] = mean_error_row_Combined[floating_columns].applymap(lambda x: qty_decimals.format(x))
            last_error_mode_row_Combined[floating_columns] = last_error_mode_row_Combined[floating_columns].applymap(lambda x: qty_decimals.format(x))
            # first concataneion of the dataframes
            combined_df_A = pd.concat([LNDCF_CFtrend_Data, header1, LNDCF_CFcycle_Data, header1], ignore_index=True)
            # concatanate the last four rows of the file
            combined_df_B = max_error_row_Combined.append([mean_error_row_Combined, last_error_mode_row_Combined], ignore_index=True)
            # second concatenation
            combined_df_LNDCF_CF_SR = pd.concat([combined_df_A, combined_df_B], ignore_index=True)
            # convert the dataframes concateneted to an output file in csv
            #combined_df_LNDCF_CF_SR.to_csv("resultsLNDCF_CF_cycle_trend_SearchRange.csv", header=True, index=True)
            banderaKnownDelay = 0

    elif preprocessing_selectionAA == 'Wavelet Denoise lvl 1' and delayMethod_selectionAA == 'Locally Normalized DCF':
        prep_technique = "WDlvl1"

        if banderaKnownDelay == 1:
            level = 1
            df_lcA_wd1, df_lcB_wd1 = waveletDenoise_function.waveletDenoise(dfA, dfB, hint_delay, level)

            LNDCF_WD1_KD = function_lndcf.find_lndcf_delay(df_lcA_wd1, df_lcB_wd1, hint_delay, prep_technique)
            #
            LNDCF_WD1_KD['LNDCF_Max'] = pd.to_numeric(LNDCF_WD1_KD['LNDCF_Max'], errors='coerce')
            LNDCF_WD1_KD['LNDCFERR'] = pd.to_numeric(LNDCF_WD1_KD['LNDCFERR'], errors='coerce')
            LNDCF_WD1_KD['EstimatedDelay'] = pd.to_numeric(LNDCF_WD1_KD['EstimatedDelay'], errors='coerce')
            LNDCF_WD1_KD['bin'] = pd.to_numeric(LNDCF_WD1_KD['bin'], errors='coerce')
            LNDCF_WD1_KD['delta min'] = pd.to_numeric(LNDCF_WD1_KD['delta min'], errors='coerce')
            LNDCF_WD1_KD['delta max'] = pd.to_numeric(LNDCF_WD1_KD['delta max'], errors='coerce')
            LNDCF_WD1_KD['uncertainty'] = pd.to_numeric(LNDCF_WD1_KD['uncertainty'], errors='coerce')
            LNDCF_WD1_KD['error'] = pd.to_numeric(LNDCF_WD1_KD['error'], errors='coerce')
            #LNDCF_WD1.to_csv("resultsLNDCF_WDlvl1_KnownDelay.csv", index=True, header=True)
            last_four_rows = LNDCF_WD1_KD.iloc[-4:]
            # row1_last_three_rows = last_four_rows.loc[last_three_rows.index[0], ['LNDCF_Max', 'EstimatedDelay', 'bin', 'delta min', 'delta max', 'uncertainty', 'error']]
            row1_preantepenultimate = last_four_rows.iloc[0]  # get first row
            row2_antepenultimate = last_four_rows.iloc[1]  # get second row
            row3_penultimate = last_four_rows.iloc[2]  # get third row
            row4_last = last_four_rows.iloc[3]  # get fourth row
                        # Call function to display the output results in a treeview
            outputResults_LNDCF.display_lndcf_results_knownDelay(frameResults, row1_preantepenultimate, row2_antepenultimate, row3_penultimate, row4_last)
            banderaSearchRange = 0
        elif banderaSearchRange == 1:
            level = 1
            df_lcA_wd1, df_lcB_wd1 = waveletDenoise_function.waveletDenoise(dfA, dfB, hint_delay, level)

            LNDCF_WD1_SR = function_lndcf.find_lndcf_delay(df_lcA_wd1, df_lcB_wd1, hint_delay, prep_technique)
            #
            LNDCF_WD1_SR['LNDCF_Max'] = pd.to_numeric(LNDCF_WD1_SR['LNDCF_Max'], errors='coerce')
            LNDCF_WD1_SR['LNDCFERR'] = pd.to_numeric(LNDCF_WD1_SR['LNDCFERR'], errors='coerce')
            LNDCF_WD1_SR['EstimatedDelay'] = pd.to_numeric(LNDCF_WD1_SR['EstimatedDelay'], errors='coerce')
            LNDCF_WD1_SR['bin'] = pd.to_numeric(LNDCF_WD1_SR['bin'], errors='coerce')
            LNDCF_WD1_SR['delta min'] = pd.to_numeric(LNDCF_WD1_SR['delta min'], errors='coerce')
            LNDCF_WD1_SR['delta max'] = pd.to_numeric(LNDCF_WD1_SR['delta max'], errors='coerce')
            LNDCF_WD1_SR['uncertainty'] = pd.to_numeric(LNDCF_WD1_SR['uncertainty'], errors='coerce')
            LNDCF_WD1_SR['error'] = pd.to_numeric(LNDCF_WD1_SR['error'], errors='coerce')

            LNDCF_WD1_SR.columns = ['LNDCF_Max', 'LNDCF_Err', 'Estimated Delay', 'bin', 'delta min', 'delta max',
                                 'search range', 'prep_technique', 'error', 'uncertainty']
            LNDCF_WD1_SR.drop('error', axis=1, inplace=True)
            LNDCF_WD1_SR.drop(LNDCF_WD1_SR.index[-4], axis=0, inplace=True)
            # Insert search range
            LNDCF_WD1_SR['search range'] = LNDCF_WD1_SR['search range'].apply(lambda x: str(input_valueCombobox))
            #LNDCF_WD1.to_csv("resultsLNDCF_WDlvl1_SearchRange.csv", index=True, header=True)
            # prepare LNDCF_SNR_Data_SR output
            last_three_rows = LNDCF_WD1_SR.iloc[-3:]
            row_1_antepenultimate = last_three_rows.iloc[0]  # get first row
            row_2_penultimate = last_three_rows.iloc[1]  # get second row
            row_3_last = last_three_rows.iloc[2]  # get third row
                        # Call function for displaying results with a search range
            outputResults_LNDCF.display_lndcf_results_searchRange(frameResults, row_1_antepenultimate, row_2_penultimate, row_3_last)
            banderaKnownDelay = 0
    elif preprocessing_selectionAA == 'Wavelet Denoise lvl 2' and delayMethod_selectionAA == 'Locally Normalized DCF':
        prep_technique = "WDlvl2"

        if banderaKnownDelay == 1:
            level = 2
            df_lcA_wd2, df_lcB_wd2 = waveletDenoise_function.waveletDenoise(dfA, dfB, hint_delay, level)

            LNDCF_WD2_KD = function_lndcf.find_lndcf_delay(df_lcA_wd2, df_lcB_wd2, hint_delay, prep_technique)
            #
            LNDCF_WD2_KD['LNDCF_Max'] = pd.to_numeric(LNDCF_WD2_KD['LNDCF_Max'], errors='coerce')
            LNDCF_WD2_KD['LNDCFERR'] = pd.to_numeric(LNDCF_WD2_KD['LNDCFERR'], errors='coerce')
            LNDCF_WD2_KD['EstimatedDelay'] = pd.to_numeric(LNDCF_WD2_KD['EstimatedDelay'], errors='coerce')
            LNDCF_WD2_KD['bin'] = pd.to_numeric(LNDCF_WD2_KD['bin'], errors='coerce')
            LNDCF_WD2_KD['delta min'] = pd.to_numeric(LNDCF_WD2_KD['delta min'], errors='coerce')
            LNDCF_WD2_KD['delta max'] = pd.to_numeric(LNDCF_WD2_KD['delta max'], errors='coerce')
            LNDCF_WD2_KD['uncertainty'] = pd.to_numeric(LNDCF_WD2_KD['uncertainty'], errors='coerce')
            LNDCF_WD2_KD['error'] = pd.to_numeric(LNDCF_WD2_KD['error'], errors='coerce')
            #LNDCF_WD2.to_csv("resultsLNDCF_" + prep_technique + "_KnownDelay.csv", index=True, header=True)
            last_four_rows = LNDCF_WD2_KD.iloc[-4:]
            row1_preantepenultimate = last_four_rows.iloc[0]  # get first row
            row2_antepenultimate = last_four_rows.iloc[1]  # get second row
            row3_penultimate = last_four_rows.iloc[2]  # get third row
            row4_last = last_four_rows.iloc[3]  # get fourth row
                        # Call function to display the output results in a treeview
            outputResults_LNDCF.display_lndcf_results_knownDelay(frameResults, row1_preantepenultimate, row2_antepenultimate, row3_penultimate, row4_last)
            banderaSearchRange = 0
        elif banderaSearchRange == 1:
            level = 2
            df_lcA_wd2, df_lcB_wd2 = waveletDenoise_function.waveletDenoise(dfA, dfB, hint_delay, level)

            LNDCF_WD2_SR = function_lndcf.find_lndcf_delay(df_lcA_wd2, df_lcB_wd2, hint_delay, prep_technique)
            #
            LNDCF_WD2_SR['LNDCF_Max'] = pd.to_numeric(LNDCF_WD2_SR['LNDCF_Max'], errors='coerce')
            LNDCF_WD2_SR['LNDCFERR'] = pd.to_numeric(LNDCF_WD2_SR['LNDCFERR'], errors='coerce')
            LNDCF_WD2_SR['EstimatedDelay'] = pd.to_numeric(LNDCF_WD2_SR['EstimatedDelay'], errors='coerce')
            LNDCF_WD2_SR['bin'] = pd.to_numeric(LNDCF_WD2_SR['bin'], errors='coerce')
            LNDCF_WD2_SR['delta min'] = pd.to_numeric(LNDCF_WD2_SR['delta min'], errors='coerce')
            LNDCF_WD2_SR['delta max'] = pd.to_numeric(LNDCF_WD2_SR['delta max'], errors='coerce')
            LNDCF_WD2_SR['uncertainty'] = pd.to_numeric(LNDCF_WD2_SR['uncertainty'], errors='coerce')
            LNDCF_WD2_SR['error'] = pd.to_numeric(LNDCF_WD2_SR['error'], errors='coerce')

            LNDCF_WD2_SR.columns = ['LNDCF_Max', 'LNDCF_Err', 'Estimated Delay', 'bin', 'delta min', 'delta max',
                                 'search range', 'prep_technique', 'error', 'uncertainty']
            LNDCF_WD2_SR.drop('error', axis=1, inplace=True)
            LNDCF_WD2_SR.drop(LNDCF_WD2_SR.index[-4], axis=0, inplace=True)
            # Insert search range
            LNDCF_WD2_SR['search range'] = LNDCF_WD2_SR['search range'].apply(lambda x: str(input_valueCombobox))
            #LNDCF_WD2.to_csv("resultsLNDCF_" + prep_technique + "_SearchRange.csv", index=True, header=True)
            # prepare LNDCF_Simple Net Return output
            last_three_rows = LNDCF_WD2_SR.iloc[-3:]
            row_1_antepenultimate = last_three_rows.iloc[0]  # get first row
            row_2_penultimate = last_three_rows.iloc[1]  # get second row
            row_3_last = last_three_rows.iloc[2]  # get third row
                        # Call function for displaying results with a search range
            outputResults_LNDCF.display_lndcf_results_searchRange(frameResults, row_1_antepenultimate, row_2_penultimate, row_3_last)
            banderaKnownDelay = 0
    elif preprocessing_selectionAA == 'Wavelet Denoise lvl 3' and delayMethod_selectionAA == 'Locally Normalized DCF':
        prep_technique = "WDlvl3"

        if banderaKnownDelay == 1:
            level = 3
            df_lcA_wd3, df_lcB_wd3 = waveletDenoise_function.waveletDenoise(dfA, dfB, hint_delay, level)

            LNDCF_WD3_KD = function_lndcf.find_lndcf_delay(df_lcA_wd3, df_lcB_wd3, hint_delay, prep_technique)
            #
            LNDCF_WD3_KD['LNDCF_Max'] = pd.to_numeric(LNDCF_WD3_KD['LNDCF_Max'], errors='coerce')
            LNDCF_WD3_KD['LNDCFERR'] = pd.to_numeric(LNDCF_WD3_KD['LNDCFERR'], errors='coerce')
            LNDCF_WD3_KD['EstimatedDelay'] = pd.to_numeric(LNDCF_WD3_KD['EstimatedDelay'], errors='coerce')
            LNDCF_WD3_KD['bin'] = pd.to_numeric(LNDCF_WD3_KD['bin'], errors='coerce')
            LNDCF_WD3_KD['delta min'] = pd.to_numeric(LNDCF_WD3_KD['delta min'], errors='coerce')
            LNDCF_WD3_KD['delta max'] = pd.to_numeric(LNDCF_WD3_KD['delta max'], errors='coerce')
            LNDCF_WD3_KD['uncertainty'] = pd.to_numeric(LNDCF_WD3_KD['uncertainty'], errors='coerce')
            LNDCF_WD3_KD['error'] = pd.to_numeric(LNDCF_WD3_KD['error'], errors='coerce')
            #LNDCF_WD3.to_csv("resultsLNDCF_" + prep_technique + "_KnownDelay.csv", index=True, header=True)
            last_four_rows = LNDCF_WD3_KD.iloc[-4:]

            row1_preantepenultimate = last_four_rows.iloc[0]  # get first row
            row2_antepenultimate = last_four_rows.iloc[1]  # get second row
            row3_penultimate = last_four_rows.iloc[2]  # get third row
            row4_last = last_four_rows.iloc[3]  # get fourth row
                        # Call function to display the output results in a treeview
            outputResults_LNDCF.display_lndcf_results_knownDelay(frameResults, row1_preantepenultimate, row2_antepenultimate, row3_penultimate, row4_last)
            banderaSearchRange = 0
        elif banderaSearchRange == 1:
            level = 3
            df_lcA_wd3, df_lcB_wd3 = waveletDenoise_function.waveletDenoise(dfA, dfB, hint_delay, level)

            LNDCF_WD3_SR = function_lndcf.find_lndcf_delay(df_lcA_wd3, df_lcB_wd3, hint_delay, prep_technique)
            #
            LNDCF_WD3_SR['LNDCF_Max'] = pd.to_numeric(LNDCF_WD3_SR['LNDCF_Max'], errors='coerce')
            LNDCF_WD3_SR['LNDCFERR'] = pd.to_numeric(LNDCF_WD3_SR['LNDCFERR'], errors='coerce')
            LNDCF_WD3_SR['EstimatedDelay'] = pd.to_numeric(LNDCF_WD3_SR['EstimatedDelay'], errors='coerce')
            LNDCF_WD3_SR['bin'] = pd.to_numeric(LNDCF_WD3_SR['bin'], errors='coerce')
            LNDCF_WD3_SR['delta min'] = pd.to_numeric(LNDCF_WD3_SR['delta min'], errors='coerce')
            LNDCF_WD3_SR['delta max'] = pd.to_numeric(LNDCF_WD3_SR['delta max'], errors='coerce')
            LNDCF_WD3_SR['uncertainty'] = pd.to_numeric(LNDCF_WD3_SR['uncertainty'], errors='coerce')
            LNDCF_WD3_SR['error'] = pd.to_numeric(LNDCF_WD3_SR['error'], errors='coerce')

            LNDCF_WD3_SR.columns = ['LNDCF_Max', 'LNDCF_Err', 'Estimated Delay', 'bin', 'delta min', 'delta max',
                                 'search range', 'prep_technique', 'error', 'uncertainty']
            LNDCF_WD3_SR.drop('error', axis=1, inplace=True)
            LNDCF_WD3_SR.drop(LNDCF_WD3_SR.index[-4], axis=0, inplace=True)
            # Insert search range
            LNDCF_WD3_SR['search range'] = LNDCF_WD3_SR['search range'].apply(lambda x: str(input_valueCombobox))
            #LNDCF_WD3.to_csv("resultsLNDCF_" + prep_technique + "_SearchRange.csv", index=True, header=True)
            # prepare LNDCF_SNR_Data_SR output
            last_three_rows = LNDCF_WD3_SR.iloc[-3:]
            row_1_antepenultimate = last_three_rows.iloc[0]  # get first row
            row_2_penultimate = last_three_rows.iloc[1]  # get second row
            row_3_last = last_three_rows.iloc[2]  # get third row
                        # Call function for displaying results with a search range
            outputResults_LNDCF.display_lndcf_results_searchRange(frameResults, row_1_antepenultimate, row_2_penultimate, row_3_last)
            banderaKnownDelay = 0
    ######################### Start of the Discrete Correlation Function (DCF)#######################
    elif preprocessing_selectionAA == 'Raw Data' and delayMethod_selectionAA == 'Discrete Correlation Function (DCF)':
        prep_technique = "Raw Data"
        df_lcA_raw, df_lcB_raw = rawData_function.raw_data(dfA, dfB, hint_delay)

        DCF_RawData = function_dcf_EK.find_dcf_delay(df_lcA_raw, df_lcB_raw, hint_delay, prep_technique)
        #
        DCF_RawData['DCF_Max'] = pd.to_numeric(DCF_RawData['DCF_Max'], errors='coerce')
        DCF_RawData['DCFERR'] = pd.to_numeric(DCF_RawData['DCFERR'], errors='coerce')
        DCF_RawData['EstimatedDelay'] = pd.to_numeric(DCF_RawData['EstimatedDelay'], errors='coerce')
        DCF_RawData['bin'] = pd.to_numeric(DCF_RawData['bin'], errors='coerce')
        DCF_RawData['delta min'] = pd.to_numeric(DCF_RawData['delta min'], errors='coerce')
        DCF_RawData['delta max'] = pd.to_numeric(DCF_RawData['delta max'], errors='coerce')
        DCF_RawData['uncertainty'] = pd.to_numeric(DCF_RawData['uncertainty'], errors='coerce')
        DCF_RawData['error'] = pd.to_numeric(DCF_RawData['error'], errors='coerce')
        if banderaKnownDelay == 1:
            #DCF_RawData.to_csv("resultsDCF_RawData_KnownDelay.csv", index=True, header=True)
            last_four_rows = DCF_RawData.iloc[-4:]

            row1_preantepenultimate = last_four_rows.iloc[0]  # get first row
            row2_antepenultimate = last_four_rows.iloc[1]  # get second row
            row3_penultimate = last_four_rows.iloc[2]  # get third row
            row4_last = last_four_rows.iloc[3]  # get fourth row
            # Call function to display the output resultswith a known delay
            outputResults_DCF.display_dcf_results_knownDelay(frameResults, row1_preantepenultimate, row2_antepenultimate, row3_penultimate, row4_last)

            banderaSearchRange = 0

        elif banderaSearchRange == 1:
            DCF_RawData.columns = ['DCF_Max', 'DCF_Err', 'EstimatedDelay', 'bin', 'delta min', 'delta max',
                                   'search range', 'prep_technique', 'error', 'uncertainty']
            DCF_RawData.drop('error', axis=1, inplace=True)
            DCF_RawData.drop(DCF_RawData.index[-4], axis=0, inplace=True)
            # Insert search range
            DCF_RawData['search range'] = DCF_RawData['search range'].apply(lambda x: str(input_valueCombobox))
            DCF_RawData_SR = DCF_RawData
            #DCF_RawData.to_csv("resultsDCF_RawData_SearchRange.csv", index=True, header=True)
            # prepare the output
            last_three_rows = DCF_RawData.iloc[-3:]
            row_1_antepenultimate = last_three_rows.iloc[0]  # get first row
            row_2_penultimate = last_three_rows.iloc[1]  # get second row
            row_3_last = last_three_rows.iloc[2]  # get third row
            # Call function for displaying results with a search range
            outputResults_DCF.display_dcf_results_searchRange(frameResults, row_1_antepenultimate, row_2_penultimate, row_3_last)
            banderaKnownDelay = 0

    elif preprocessing_selectionAA == 'Data Differencing' and delayMethod_selectionAA == 'Discrete Correlation Function (DCF)':
        prep_technique = "Differencing"

        if banderaKnownDelay == 1:
            df_lcA_diff, df_lcB_diff = data_differencing_function.data_differencing(dfA, dfB, hint_delay)

            DCF_DiffData = function_dcf_EK.find_dcf_delay(df_lcA_diff, df_lcB_diff, hint_delay, prep_technique)
            #
            DCF_DiffData['DCF_Max'] = pd.to_numeric(DCF_DiffData['DCF_Max'], errors='coerce')
            DCF_DiffData['DCFERR'] = pd.to_numeric(DCF_DiffData['DCFERR'], errors='coerce')
            DCF_DiffData['EstimatedDelay'] = pd.to_numeric(DCF_DiffData['EstimatedDelay'], errors='coerce')
            DCF_DiffData['bin'] = pd.to_numeric(DCF_DiffData['bin'], errors='coerce')
            DCF_DiffData['delta min'] = pd.to_numeric(DCF_DiffData['delta min'], errors='coerce')
            DCF_DiffData['delta max'] = pd.to_numeric(DCF_DiffData['delta max'], errors='coerce')
            DCF_DiffData['uncertainty'] = pd.to_numeric(DCF_DiffData['uncertainty'], errors='coerce')
            DCF_DiffData['error'] = pd.to_numeric(DCF_DiffData['error'], errors='coerce')
            #DCF_DiffData.to_csv("resultsDCF_Differencing_KnownDelay.csv", index=True, header=True)
            last_four_rows = DCF_DiffData.iloc[-4:]

            row1_preantepenultimate = last_four_rows.iloc[0]  # get first row
            row2_antepenultimate = last_four_rows.iloc[1]  # get second row
            row3_penultimate = last_four_rows.iloc[2]  # get third row
            row4_last = last_four_rows.iloc[3]  # get fourth row
            # Call function for displaying results with known delay
            outputResults_DCF.display_dcf_results_knownDelay(frameResults, row1_preantepenultimate, row2_antepenultimate, row3_penultimate, row4_last)
            banderaSearchRange = 0

        elif banderaSearchRange == 1:
            df_lcA_diff_sr, df_lcB_diff_sr = data_differencing_function.data_differencing(dfA, dfB, hint_delay)
            DCF_DiffData_SR = function_dcf_EK.find_dcf_delay(df_lcA_diff_sr, df_lcB_diff_sr, hint_delay, prep_technique)
            #
            DCF_DiffData_SR['DCF_Max'] = pd.to_numeric(DCF_DiffData_SR['DCF_Max'], errors='coerce')
            DCF_DiffData_SR['DCFERR'] = pd.to_numeric(DCF_DiffData_SR['DCFERR'], errors='coerce')
            DCF_DiffData_SR['EstimatedDelay'] = pd.to_numeric(DCF_DiffData_SR['EstimatedDelay'], errors='coerce')
            DCF_DiffData_SR['bin'] = pd.to_numeric(DCF_DiffData_SR['bin'], errors='coerce')
            DCF_DiffData_SR['delta min'] = pd.to_numeric(DCF_DiffData_SR['delta min'], errors='coerce')
            DCF_DiffData_SR['delta max'] = pd.to_numeric(DCF_DiffData_SR['delta max'], errors='coerce')
            DCF_DiffData_SR['uncertainty'] = pd.to_numeric(DCF_DiffData_SR['uncertainty'], errors='coerce')
            DCF_DiffData_SR['error'] = pd.to_numeric(DCF_DiffData_SR['error'], errors='coerce')

            DCF_DiffData_SR.columns = ['DCF_Max', 'DCF_Err', 'EstimatedDelay', 'bin', 'delta min', 'delta max',
                                       'search range', 'prep_technique', 'error', 'uncertainty']
            DCF_DiffData_SR.drop('error', axis=1, inplace=True)
            DCF_DiffData_SR.drop(DCF_DiffData_SR.index[-4], axis=0, inplace=True)
            # Insert search range
            DCF_DiffData_SR['search range'] = DCF_DiffData_SR['search range'].apply(lambda x: str(input_valueCombobox))
            #DCF_DiffData_SR.to_csv("resultsDCF_Differencing_SearchRange.csv", index=True, header=True)
            # prepare LNDCF Data Differencing output
            last_three_rows = DCF_DiffData_SR.iloc[-3:]
            row_1_antepenultimate = last_three_rows.iloc[0]  # get first row
            row_2_penultimate = last_three_rows.iloc[1]  # get second row
            row_3_last = last_three_rows.iloc[2]  # get third row
                        # Call function for displaying results with a search range
            outputResults_DCF.display_dcf_results_searchRange(frameResults, row_1_antepenultimate, row_2_penultimate, row_3_last)
            banderaKnownDelay = 0

    elif preprocessing_selectionAA == 'Simple Net Return' and delayMethod_selectionAA == 'Discrete Correlation Function (DCF)':
        prep_technique = "SimpleNetReturn"

        if banderaKnownDelay == 1:
            df_lcA_snr, df_lcB_snr = simpleNetReturn_function.simple_net_return(dfA, dfB, hint_delay)

            DCF_SNR_Data = function_dcf_EK.find_dcf_delay(df_lcA_snr, df_lcB_snr, hint_delay, prep_technique)
            #
            DCF_SNR_Data['DCF_Max'] = pd.to_numeric(DCF_SNR_Data['DCF_Max'], errors='coerce')
            DCF_SNR_Data['DCFERR'] = pd.to_numeric(DCF_SNR_Data['DCFERR'], errors='coerce')
            DCF_SNR_Data['EstimatedDelay'] = pd.to_numeric(DCF_SNR_Data['EstimatedDelay'], errors='coerce')
            DCF_SNR_Data['bin'] = pd.to_numeric(DCF_SNR_Data['bin'], errors='coerce')
            DCF_SNR_Data['delta min'] = pd.to_numeric(DCF_SNR_Data['delta min'], errors='coerce')
            DCF_SNR_Data['delta max'] = pd.to_numeric(DCF_SNR_Data['delta max'], errors='coerce')
            DCF_SNR_Data['uncertainty'] = pd.to_numeric(DCF_SNR_Data['uncertainty'], errors='coerce')
            DCF_SNR_Data['error'] = pd.to_numeric(DCF_SNR_Data['error'], errors='coerce')

            #DCF_SNR_Data.to_csv("resultsDCF_SimpleNetReturn_KnownDelay.csv", index=True, header=True)
            last_four_rows = DCF_SNR_Data.iloc[-4:]

            row1_preantepenultimate = last_four_rows.iloc[0]  # get first row
            row2_antepenultimate = last_four_rows.iloc[1]  # get second row
            row3_penultimate = last_four_rows.iloc[2]  # get third row
            row4_last = last_four_rows.iloc[3]  # get fourth row
            # Call function for displaying results with known delay
            outputResults_DCF.display_dcf_results_knownDelay(frameResults, row1_preantepenultimate, row2_antepenultimate, row3_penultimate, row4_last)
            banderaSearchRange = 0
        elif banderaSearchRange == 1:
            df_lcA_snr, df_lcB_snr = simpleNetReturn_function.simple_net_return(dfA, dfB, hint_delay)

            DCF_SNR_Data_SR = function_dcf_EK.find_dcf_delay(df_lcA_snr, df_lcB_snr, hint_delay, prep_technique)
            #
            DCF_SNR_Data_SR['DCF_Max'] = pd.to_numeric(DCF_SNR_Data_SR['DCF_Max'], errors='coerce')
            DCF_SNR_Data_SR['DCFERR'] = pd.to_numeric(DCF_SNR_Data_SR['DCFERR'], errors='coerce')
            DCF_SNR_Data_SR['EstimatedDelay'] = pd.to_numeric(DCF_SNR_Data_SR['EstimatedDelay'], errors='coerce')
            DCF_SNR_Data_SR['bin'] = pd.to_numeric(DCF_SNR_Data_SR['bin'], errors='coerce')
            DCF_SNR_Data_SR['delta min'] = pd.to_numeric(DCF_SNR_Data_SR['delta min'], errors='coerce')
            DCF_SNR_Data_SR['delta max'] = pd.to_numeric(DCF_SNR_Data_SR['delta max'], errors='coerce')
            DCF_SNR_Data_SR['uncertainty'] = pd.to_numeric(DCF_SNR_Data_SR['uncertainty'], errors='coerce')
            DCF_SNR_Data_SR['error'] = pd.to_numeric(DCF_SNR_Data_SR['error'], errors='coerce')

            DCF_SNR_Data_SR.columns = ['DCF_Max', 'DCFERR', 'EstimatedDelay', 'bin', 'delta min', 'delta max',
                                       'search range', 'prep_technique', 'error', 'uncertainty']
            DCF_SNR_Data_SR.drop('error', axis=1, inplace=True)
            DCF_SNR_Data_SR.drop(DCF_SNR_Data_SR.index[-4], axis=0, inplace=True)
            # Insert search range
            DCF_SNR_Data_SR['search range'] = DCF_SNR_Data_SR['search range'].apply(lambda x: str(input_valueCombobox))
            #DCF_SNR_Data_sr.to_csv("resultsDCF_SimpleNetReturn_SearchRange.csv", index=True, header=True)
            # prepare LNDCF_SNR_Data_SR output
            last_three_rows = DCF_SNR_Data_SR.iloc[-3:]
            row_1_antepenultimate = last_three_rows.iloc[0]  # get first row
            row_2_penultimate = last_three_rows.iloc[1]  # get second row
            row_3_last = last_three_rows.iloc[2]  # get third row
                        # Call function for displaying results with a search range
            outputResults_DCF.display_dcf_results_searchRange(frameResults, row_1_antepenultimate, row_2_penultimate, row_3_last)
            banderaKnownDelay = 0

    elif preprocessing_selectionAA == "Christiano-Fitzgerald filter" and delayMethod_selectionAA == "Discrete Correlation Function (DCF)":
        prep_techniqueA = "CF-trend"
        prep_techniqueB = "CF-cycle"

        if banderaKnownDelay == 1:
            # obtain cycle and trend of CF filter
            dfCycle_lcA, dfCycle_lcB, dfTrend_lcA, dfTrend_lcB = CFfilter_function.cf_filter(dfA, dfB, hint_delay)

            DCF_CFcycle_Data = function_dcf_EK.find_dcf_delay(dfCycle_lcA, dfCycle_lcB, hint_delay, prep_techniqueB)

            DCF_CFtrend_Data = function_dcf_EK.find_dcf_delay(dfTrend_lcA, dfTrend_lcB, hint_delay, prep_techniqueA)
            #
            # Ensure that the following columns are numeric for format output
            DCF_CFtrend_Data['DCF_Max'] = pd.to_numeric(DCF_CFtrend_Data['DCF_Max'], errors='coerce')
            DCF_CFtrend_Data['DCFERR'] = pd.to_numeric(DCF_CFtrend_Data['DCFERR'], errors='coerce')
            DCF_CFtrend_Data['EstimatedDelay'] = pd.to_numeric(DCF_CFtrend_Data['EstimatedDelay'], errors='coerce')
            DCF_CFtrend_Data['bin'] = pd.to_numeric(DCF_CFtrend_Data['bin'], errors='coerce')
            DCF_CFtrend_Data['delta min'] = pd.to_numeric(DCF_CFtrend_Data['delta min'], errors='coerce')
            DCF_CFtrend_Data['delta max'] = pd.to_numeric(DCF_CFtrend_Data['delta max'], errors='coerce')
            DCF_CFtrend_Data['uncertainty'] = pd.to_numeric(DCF_CFtrend_Data['uncertainty'], errors='coerce')
            DCF_CFtrend_Data['error'] = pd.to_numeric(DCF_CFtrend_Data['error'], errors='coerce')
            # Ensure that the following columns are numeric for format output
            DCF_CFcycle_Data['DCF_Max'] = pd.to_numeric(DCF_CFcycle_Data['DCF_Max'], errors='coerce')
            DCF_CFcycle_Data['DCFERR'] = pd.to_numeric(DCF_CFcycle_Data['DCFERR'], errors='coerce')
            DCF_CFcycle_Data['EstimatedDelay'] = pd.to_numeric(DCF_CFcycle_Data['EstimatedDelay'], errors='coerce')
            DCF_CFcycle_Data['bin'] = pd.to_numeric(DCF_CFcycle_Data['bin'], errors='coerce')
            DCF_CFcycle_Data['delta min'] = pd.to_numeric(DCF_CFcycle_Data['delta min'], errors='coerce')
            DCF_CFcycle_Data['delta max'] = pd.to_numeric(DCF_CFcycle_Data['delta max'], errors='coerce')
            DCF_CFcycle_Data['uncertainty'] = pd.to_numeric(DCF_CFcycle_Data['uncertainty'], errors='coerce')
            DCF_CFcycle_Data['error'] = pd.to_numeric(DCF_CFcycle_Data['error'], errors='coerce')
            # obtain the last four rows from cycle
            last_fourth_cycle_rows = DCF_CFcycle_Data.iloc[-4:]
            row_one_min_cycle_preantepenultimate = last_fourth_cycle_rows.iloc[0]  # get first row
            row_two_max_cycle_antepenultimate = last_fourth_cycle_rows.iloc[1]  # get second row
            row_three_mean_cycle_penultimate = last_fourth_cycle_rows.iloc[2]  # get third row
            row_four_mode_cycle_last = last_fourth_cycle_rows.iloc[3]  # get fourth row
            # obtain the last four rows from trend
            last_fourth_trend_rows = DCF_CFtrend_Data.iloc[-4:]
            row_one_min_trend_preantepenultimate = last_fourth_trend_rows.iloc[0]  # get first row
            row_two_max_trend_antepenultimate = last_fourth_trend_rows.iloc[1]  # get second row
            row_three_mean_trend_penultimate = last_fourth_trend_rows.iloc[2]  # get third row
            row_four_mode_trend_last = last_fourth_trend_rows.iloc[3]  # get fourth row
            # Calculate the combined min error
            min_error_row_Combined = pd.DataFrame({
                'DCF_Max': (row_one_min_cycle_preantepenultimate["DCF_Max"] + row_one_min_trend_preantepenultimate["DCF_Max"]) / 2,
                'DCFERR': (row_one_min_cycle_preantepenultimate["DCFERR"] + row_one_min_trend_preantepenultimate["DCFERR"]) / 2,
                'EstimatedDelay': (row_one_min_cycle_preantepenultimate["EstimatedDelay"] +
                                   row_one_min_trend_preantepenultimate["EstimatedDelay"]) / 2,
                'bin': (row_one_min_cycle_preantepenultimate['bin'] + row_one_min_trend_preantepenultimate["bin"]) / 2,
                'delta min': (row_one_min_cycle_preantepenultimate['delta min'] + row_one_min_trend_preantepenultimate["delta min"]) / 2,
                'delta max': (row_one_min_cycle_preantepenultimate["delta max"] + row_one_min_trend_preantepenultimate["delta max"]) / 2,
                'True delay': row_one_min_cycle_preantepenultimate["True delay"],
                'prep_technique': row_one_min_cycle_preantepenultimate["prep_technique"],
                'uncertainty': (row_one_min_cycle_preantepenultimate['uncertainty'] + row_one_min_trend_preantepenultimate['uncertainty']) / 2,
                'error': abs(((row_one_min_cycle_preantepenultimate["EstimatedDelay"] +
                               row_one_min_trend_preantepenultimate["EstimatedDelay"]) / 2) -
                          row_one_min_cycle_preantepenultimate["True delay"])}, index=[0])
            min_error_row_Combined.iloc[0, -3] = 'min trend/cycle'
            # Calculate the combined mean
            max_error_row_Combined = pd.DataFrame({
                'DCF_Max': (row_two_max_cycle_antepenultimate["DCF_Max"] + row_two_max_trend_antepenultimate["DCF_Max"]) / 2,
                'DCFERR': (row_two_max_cycle_antepenultimate["DCFERR"] + row_two_max_trend_antepenultimate["DCFERR"]) / 2,
                'EstimatedDelay': (row_two_max_cycle_antepenultimate["EstimatedDelay"] +
                                   row_two_max_trend_antepenultimate["EstimatedDelay"]) / 2,
                'bin': (row_two_max_cycle_antepenultimate['bin'] + row_two_max_trend_antepenultimate["bin"]) / 2,
                'delta min': (row_two_max_cycle_antepenultimate['delta min'] + row_two_max_trend_antepenultimate["delta min"]) / 2,
                'delta max': (row_two_max_cycle_antepenultimate["delta max"] + row_two_max_trend_antepenultimate["delta max"]) / 2,
                'True delay': row_two_max_cycle_antepenultimate["True delay"],
                'prep_technique': row_two_max_cycle_antepenultimate["prep_technique"],
                'uncertainty': (row_two_max_cycle_antepenultimate['uncertainty'] + row_two_max_trend_antepenultimate['uncertainty']) / 2,
                'error': abs(((row_two_max_cycle_antepenultimate["EstimatedDelay"] + row_two_max_trend_antepenultimate[
                    "EstimatedDelay"]) / 2) - row_two_max_cycle_antepenultimate["True delay"])}, index=[0])
            max_error_row_Combined.iloc[0, -3] = 'max trend/cycle'
            # Calculate the combined mode
            mean_error_row_Combined = pd.DataFrame({
                'DCF_Max': (row_three_mean_cycle_penultimate["DCF_Max"] + row_three_mean_trend_penultimate["DCF_Max"]) / 2,
                'DCFERR': (row_three_mean_cycle_penultimate["DCFERR"] + row_three_mean_trend_penultimate["DCFERR"]) / 2,
                'EstimatedDelay': (row_three_mean_cycle_penultimate["EstimatedDelay"] + row_three_mean_trend_penultimate["EstimatedDelay"]) / 2,
                'bin': (row_three_mean_cycle_penultimate['bin'] + row_three_mean_trend_penultimate["bin"]) / 2,
                'delta min': (row_three_mean_cycle_penultimate['delta min'] + row_three_mean_trend_penultimate["delta min"]) / 2,
                'delta max': (row_three_mean_cycle_penultimate["delta max"] + row_three_mean_trend_penultimate["delta max"]) / 2,
                'True delay': row_three_mean_cycle_penultimate["True delay"],
                'prep_technique': row_three_mean_cycle_penultimate["prep_technique"],
                'uncertainty': (row_three_mean_cycle_penultimate['uncertainty'] + row_three_mean_trend_penultimate['uncertainty']) / 2,
                'error': abs(((row_three_mean_cycle_penultimate["EstimatedDelay"] + row_three_mean_trend_penultimate[
                    "EstimatedDelay"]) / 2) - row_three_mean_cycle_penultimate["True delay"])}, index=[0])
            mean_error_row_Combined.iloc[0, -3] = 'mean trend/cycle'
            # Calculate the average of the combined mean and mode
            last_mode_error_row_Combined = pd.DataFrame({
                'DCF_Max': (row_four_mode_cycle_last["DCF_Max"] + row_four_mode_trend_last["DCF_Max"]) / 2,
                'DCFERR': (row_four_mode_cycle_last["DCFERR"] + row_four_mode_trend_last["DCFERR"]) / 2,
                'EstimatedDelay': (row_four_mode_cycle_last["EstimatedDelay"] + row_four_mode_trend_last["EstimatedDelay"]) / 2,
                'bin': (row_four_mode_cycle_last['bin'] + row_four_mode_trend_last["bin"]) / 2,
                'delta min': (row_four_mode_cycle_last['delta min'] + row_four_mode_trend_last["delta min"]) / 2,
                'delta max': (row_four_mode_cycle_last["delta max"] + row_four_mode_trend_last["delta max"]) / 2,
                'True delay': row_four_mode_cycle_last["True delay"],
                'prep_technique': row_four_mode_cycle_last["prep_technique"],
                'uncertainty': (row_four_mode_cycle_last['uncertainty'] + row_four_mode_trend_last['uncertainty']) / 2,
                'error': abs(((row_four_mode_cycle_last["EstimatedDelay"] + row_four_mode_trend_last[
                    "EstimatedDelay"]) / 2) - row_four_mode_cycle_last["True delay"])}, index=[0])
            last_mode_error_row_Combined.iloc[0, -3] = 'mode trend/cycle'
            # Create a header to insert to the concatenated DataFrames
            header1 = pd.DataFrame([{'DCF_Max': 'DCF_Max', 'DCFERR': 'DCFERR', 'EstimatedDelay': 'EstimatedDelay',
                                     'bin': 'bin', 'delta min': 'delta min', 'delta max': 'delta max',
                                     'True delay': 'True delay', 'prep_technique': 'prep_technique',
                                     'uncertainty': 'uncertainty', 'error': 'error'}])
            # Ensure that the following columns are numeric for format output
            min_error_row_Combined['DCF_Max'] = pd.to_numeric(min_error_row_Combined['DCF_Max'], errors='coerce')
            min_error_row_Combined['DCFERR'] = pd.to_numeric(min_error_row_Combined['DCFERR'], errors='coerce')
            min_error_row_Combined['EstimatedDelay'] = pd.to_numeric(min_error_row_Combined['EstimatedDelay'], errors='coerce')
            min_error_row_Combined['bin'] = pd.to_numeric(min_error_row_Combined['bin'], errors='coerce')
            min_error_row_Combined['delta min'] = pd.to_numeric(min_error_row_Combined['delta min'], errors='coerce')
            min_error_row_Combined['delta max'] = pd.to_numeric(min_error_row_Combined['delta max'], errors='coerce')
            min_error_row_Combined['uncertainty'] = pd.to_numeric(min_error_row_Combined['uncertainty'], errors='coerce')
            min_error_row_Combined['error'] = pd.to_numeric(min_error_row_Combined['error'], errors='coerce')
            # Ensure that the following columns are numeric for format output
            max_error_row_Combined['DCF_Max'] = pd.to_numeric(max_error_row_Combined['DCF_Max'], errors='coerce')
            max_error_row_Combined['DCFERR'] = pd.to_numeric(max_error_row_Combined['DCFERR'], errors='coerce')
            max_error_row_Combined['EstimatedDelay'] = pd.to_numeric(max_error_row_Combined['EstimatedDelay'], errors='coerce')
            max_error_row_Combined['bin'] = pd.to_numeric(max_error_row_Combined['bin'], errors='coerce')
            max_error_row_Combined['delta min'] = pd.to_numeric(max_error_row_Combined['delta min'], errors='coerce')
            max_error_row_Combined['delta max'] = pd.to_numeric(max_error_row_Combined['delta max'], errors='coerce')
            max_error_row_Combined['uncertainty'] = pd.to_numeric(max_error_row_Combined['uncertainty'], errors='coerce')
            max_error_row_Combined['error'] = pd.to_numeric(max_error_row_Combined['error'], errors='coerce')
            # Ensure that the following columns are numeric for format output
            mean_error_row_Combined['DCF_Max'] = pd.to_numeric(mean_error_row_Combined['DCF_Max'], errors='coerce')
            mean_error_row_Combined['DCFERR'] = pd.to_numeric(mean_error_row_Combined['DCFERR'], errors='coerce')
            mean_error_row_Combined['EstimatedDelay'] = pd.to_numeric(mean_error_row_Combined['EstimatedDelay'], errors='coerce')
            mean_error_row_Combined['bin'] = pd.to_numeric(mean_error_row_Combined['bin'], errors='coerce')
            mean_error_row_Combined['delta min'] = pd.to_numeric(mean_error_row_Combined['delta min'], errors='coerce')
            mean_error_row_Combined['delta max'] = pd.to_numeric(mean_error_row_Combined['delta max'], errors='coerce')
            mean_error_row_Combined['uncertainty'] = pd.to_numeric(mean_error_row_Combined['uncertainty'], errors='coerce')
            mean_error_row_Combined['error'] = pd.to_numeric(mean_error_row_Combined['error'], errors='coerce')
            # Ensure that the following columns are numeric for format output
            last_mode_error_row_Combined['DCF_Max'] = pd.to_numeric(last_mode_error_row_Combined['DCF_Max'], errors='coerce')
            last_mode_error_row_Combined['DCFERR'] = pd.to_numeric(last_mode_error_row_Combined['DCFERR'], errors='coerce')
            last_mode_error_row_Combined['EstimatedDelay'] = pd.to_numeric(last_mode_error_row_Combined['EstimatedDelay'], errors='coerce')
            last_mode_error_row_Combined['bin'] = pd.to_numeric(last_mode_error_row_Combined['bin'], errors='coerce')
            last_mode_error_row_Combined['delta min'] = pd.to_numeric(last_mode_error_row_Combined['delta min'], errors='coerce')
            last_mode_error_row_Combined['delta max'] = pd.to_numeric(last_mode_error_row_Combined['delta max'], errors='coerce')
            last_mode_error_row_Combined['uncertainty'] = pd.to_numeric(last_mode_error_row_Combined['uncertainty'], errors='coerce')
            last_mode_error_row_Combined['error'] = pd.to_numeric(last_mode_error_row_Combined['error'], errors='coerce')
            # Convert each DataFrame into a Series by selecting the first row
            min_error_preantepenultimate = min_error_row_Combined.iloc[0]
            max_error_antepenultimate = max_error_row_Combined.iloc[0]
            mean_error_penultimate = mean_error_row_Combined.iloc[0]
            last_mode_error_last = last_mode_error_row_Combined.iloc[0]
                                    # Call function to display the output results in a treeview
            outputResults_DCF.display_dcf_results_knownDelay(frameResults, min_error_preantepenultimate, max_error_antepenultimate, mean_error_penultimate, last_mode_error_last)
            # The next code is for creating a csv file for output
            # Define the format for numeric columns
            qty_decimals = '{:.4f}'  # Choosed the number of four decimal places
            # Apply formatting to specific numeric columns
            floating_columns = ['DCF_Max', 'DCFERR', 'EstimatedDelay', 'bin', 'delta min', 'delta max', 'uncertainty','error']
            DCF_CFcycle_Data[floating_columns] = DCF_CFcycle_Data[floating_columns].applymap(lambda x: qty_decimals.format(x))
            DCF_CFtrend_Data[floating_columns] = DCF_CFtrend_Data[floating_columns].applymap(lambda x: qty_decimals.format(x))
            ##
            min_error_row_Combined[floating_columns] = min_error_row_Combined[floating_columns].applymap(lambda x: qty_decimals.format(x))
            max_error_row_Combined[floating_columns] = max_error_row_Combined[floating_columns].applymap(lambda x: qty_decimals.format(x))
            mean_error_row_Combined[floating_columns] = mean_error_row_Combined[floating_columns].applymap(lambda x: qty_decimals.format(x))
            last_mode_error_row_Combined[floating_columns] = last_mode_error_row_Combined[floating_columns].applymap(lambda x: qty_decimals.format(x))
            # first concataneion of the dataframes
            combined_df_A = pd.concat([DCF_CFtrend_Data, header1, DCF_CFcycle_Data, header1], ignore_index=True)
            # concatanate the last four rows of the file
            combined_df_B = min_error_row_Combined.append([max_error_row_Combined, mean_error_row_Combined, last_mode_error_row_Combined], ignore_index=True)
            # second concatenation
            combined_df_DFC_KD = pd.concat([combined_df_A, combined_df_B], ignore_index=True)
            # convert the dataframes concateneted to an output file in csv
            #combined_df_C.to_csv("resultsDCF_CF_cycle_trend_KnownDelay.csv", header=True, index=True)
            banderaSearchRange = 0
        elif banderaSearchRange == 1:
            # obtain cycle and trend of CF filter
            dfCycle_lcA, dfCycle_lcB, dfTrend_lcA, dfTrend_lcB = CFfilter_function.cf_filter(dfA, dfB, hint_delay)

            DCF_CFcycle_Data = function_dcf_EK.find_dcf_delay(dfCycle_lcA, dfCycle_lcB, hint_delay, prep_techniqueB)

            DCF_CFtrend_Data = function_dcf_EK.find_dcf_delay(dfTrend_lcA, dfTrend_lcB, hint_delay, prep_techniqueA)
            # Ensure that the following columns are numeric for format output
            DCF_CFtrend_Data['DCF_Max'] = pd.to_numeric(DCF_CFtrend_Data['DCF_Max'], errors='coerce')
            DCF_CFtrend_Data['DCFERR'] = pd.to_numeric(DCF_CFtrend_Data['DCFERR'], errors='coerce')
            DCF_CFtrend_Data['EstimatedDelay'] = pd.to_numeric(DCF_CFtrend_Data['EstimatedDelay'], errors='coerce')
            DCF_CFtrend_Data['bin'] = pd.to_numeric(DCF_CFtrend_Data['bin'], errors='coerce')
            DCF_CFtrend_Data['delta min'] = pd.to_numeric(DCF_CFtrend_Data['delta min'], errors='coerce')
            DCF_CFtrend_Data['delta max'] = pd.to_numeric(DCF_CFtrend_Data['delta max'], errors='coerce')
            DCF_CFtrend_Data['uncertainty'] = pd.to_numeric(DCF_CFtrend_Data['uncertainty'], errors='coerce')
            DCF_CFtrend_Data['error'] = pd.to_numeric(DCF_CFtrend_Data['error'], errors='coerce')
            # Ensure that the following columns are numeric for format output
            DCF_CFcycle_Data['DCF_Max'] = pd.to_numeric(DCF_CFcycle_Data['DCF_Max'], errors='coerce')
            DCF_CFcycle_Data['DCFERR'] = pd.to_numeric(DCF_CFcycle_Data['DCFERR'], errors='coerce')
            DCF_CFcycle_Data['EstimatedDelay'] = pd.to_numeric(DCF_CFcycle_Data['EstimatedDelay'], errors='coerce')
            DCF_CFcycle_Data['bin'] = pd.to_numeric(DCF_CFcycle_Data['bin'], errors='coerce')
            DCF_CFcycle_Data['delta min'] = pd.to_numeric(DCF_CFcycle_Data['delta min'], errors='coerce')
            DCF_CFcycle_Data['delta max'] = pd.to_numeric(DCF_CFcycle_Data['delta max'], errors='coerce')
            DCF_CFcycle_Data['uncertainty'] = pd.to_numeric(DCF_CFcycle_Data['uncertainty'], errors='coerce')
            DCF_CFcycle_Data['error'] = pd.to_numeric(DCF_CFcycle_Data['error'], errors='coerce')

            DCF_CFtrend_Data.columns = ['DCF_Max', 'DCFERR', 'EstimatedDelay', 'bin', 'delta min', 'delta max',
                                        'search range', 'prep_technique', 'uncertainty', 'error']
            DCF_CFcycle_Data.columns = ['DCF_Max', 'DCFERR', 'EstimatedDelay', 'bin', 'delta min', 'delta max',
                                        'search range', 'prep_technique', 'uncertainty', 'error']
            DCF_CFtrend_Data.drop('error', axis=1, inplace=True)
            DCF_CFtrend_Data.drop(DCF_CFtrend_Data.index[-4], axis=0, inplace=True)
            DCF_CFcycle_Data.drop('error', axis=1, inplace=True)
            DCF_CFcycle_Data.drop(DCF_CFcycle_Data.index[-4], axis=0, inplace=True)
            # Insert search range
            DCF_CFcycle_Data['search range'] = DCF_CFcycle_Data['search range'].apply(lambda x: str(input_valueCombobox))
            DCF_CFtrend_Data['search range'] = DCF_CFtrend_Data['search range'].apply(lambda x: str(input_valueCombobox))
            # obtain the last three rows from cycle
            last_three_cycle_rows = DCF_CFcycle_Data.iloc[-3:]
            row_one_max_cycle_antepenultimate = last_three_cycle_rows.iloc[0]  # get second row
            row_two_mean_cycle_penultimate = last_three_cycle_rows.iloc[1]  # get third row
            row_three_mode_cycle_last = last_three_cycle_rows.iloc[2]  # get fourth row
            # obtain the last four rows from trend
            last_three_trend_rows = DCF_CFtrend_Data.iloc[-3:]
            row_one_max_trend_antepenultimate = last_three_trend_rows.iloc[0]  # get second row
            row_two_mean_trend_penultimate = last_three_trend_rows.iloc[1]  # get third row
            row_three_mode_trend_last = last_three_trend_rows.iloc[2]  # get fourth row
            # Calculate the combined mean
            max_error_row_Combined = pd.DataFrame({
                'DCF_Max': (row_one_max_cycle_antepenultimate["DCF_Max"] + row_one_max_trend_antepenultimate["DCF_Max"]) / 2,
                'DCFERR': (row_one_max_cycle_antepenultimate["DCFERR"] + row_one_max_trend_antepenultimate["DCFERR"]) / 2,
                'EstimatedDelay': (row_one_max_cycle_antepenultimate["EstimatedDelay"] +
                                    row_one_max_trend_antepenultimate["EstimatedDelay"]) / 2,
                'bin': (row_one_max_cycle_antepenultimate['bin'] + row_one_max_trend_antepenultimate["bin"]) / 2,
                'delta min': (row_one_max_cycle_antepenultimate['delta min'] + row_one_max_trend_antepenultimate["delta min"]) / 2,
                'delta max': (row_one_max_cycle_antepenultimate["delta max"] + row_one_max_trend_antepenultimate["delta max"]) / 2,
                'search range': row_one_max_cycle_antepenultimate["search range"],
                'prep_technique': row_one_max_cycle_antepenultimate["prep_technique"],
                'uncertainty': (row_one_max_cycle_antepenultimate['uncertainty'] + row_one_max_trend_antepenultimate['uncertainty']) / 2}, index=[0])
            max_error_row_Combined.iloc[0, -2] = 'max trend/cycle'
            # Calculate the combined mode
            mean_error_row_Combined = pd.DataFrame({
                'DCF_Max': (row_two_mean_cycle_penultimate["DCF_Max"] + row_two_mean_trend_penultimate["DCF_Max"]) / 2,
                'DCFERR': (row_two_mean_cycle_penultimate["DCFERR"] + row_two_mean_trend_penultimate["DCFERR"]) / 2,
                'EstimatedDelay': (row_two_mean_cycle_penultimate["EstimatedDelay"] + row_two_mean_trend_penultimate["EstimatedDelay"]) / 2,
                'bin': (row_two_mean_cycle_penultimate['bin'] + row_two_mean_trend_penultimate["bin"]) / 2,
                'delta min': (row_two_mean_cycle_penultimate['delta min'] + row_two_mean_trend_penultimate["delta min"]) / 2,
                'delta max': (row_two_mean_cycle_penultimate["delta max"] + row_two_mean_trend_penultimate["delta max"]) / 2,
                'search range': row_two_mean_cycle_penultimate["search range"],
                'prep_technique': row_two_mean_cycle_penultimate["prep_technique"],
                'uncertainty': (row_two_mean_cycle_penultimate['uncertainty'] + row_two_mean_trend_penultimate[
                    'uncertainty']) / 2}, index=[0])
            mean_error_row_Combined.iloc[0, -2] = 'mean trend/cycle'
            # Calculate the average of the combined mean and mode
            last_error_mode_row_Combined = pd.DataFrame({
                'DCF_Max': (row_three_mode_cycle_last["DCF_Max"] + row_three_mode_trend_last["DCF_Max"]) / 2,
                'DCFERR': (row_three_mode_cycle_last["DCFERR"] + row_three_mode_trend_last["DCFERR"]) / 2,
                'EstimatedDelay': (row_three_mode_cycle_last["EstimatedDelay"] + row_three_mode_trend_last["EstimatedDelay"]) / 2,
                'bin': (row_three_mode_cycle_last['bin'] + row_three_mode_trend_last["bin"]) / 2,
                'delta min': (row_three_mode_cycle_last['delta min'] + row_three_mode_trend_last["delta min"]) / 2,
                'delta max': (row_three_mode_cycle_last["delta max"] + row_three_mode_trend_last["delta max"]) / 2,
                'search range': row_three_mode_cycle_last["search range"],
                'prep_technique': row_three_mode_cycle_last["prep_technique"],
                'uncertainty': (row_three_mode_cycle_last['uncertainty'] + row_three_mode_trend_last['uncertainty']) / 2}, index=[0])
            last_error_mode_row_Combined.iloc[0, -2] = 'mode trend/cycle'
            # Create a header to insert to the concatenated DataFrames
            header1 = pd.DataFrame([{'DCF_Max': 'DCF_Max', 'DCFERR': 'DCFERR', 'EstimatedDelay': 'EstimatedDelay',
                                     'bin': 'bin', 'delta min': 'delta min', 'delta max': 'delta max',
                                     'search range': 'search range', 'prep_technique': 'prep_technique',
                                     'uncertainty': 'uncertainty'}])
            # Ensure that the following columns are numeric for format output
            max_error_row_Combined['DCF_Max'] = pd.to_numeric(max_error_row_Combined['DCF_Max'], errors='coerce')
            max_error_row_Combined['DCFERR'] = pd.to_numeric(max_error_row_Combined['DCFERR'], errors='coerce')
            max_error_row_Combined['EstimatedDelay'] = pd.to_numeric(max_error_row_Combined['EstimatedDelay'], errors='coerce')
            max_error_row_Combined['bin'] = pd.to_numeric(max_error_row_Combined['bin'], errors='coerce')
            max_error_row_Combined['delta min'] = pd.to_numeric(max_error_row_Combined['delta min'], errors='coerce')
            max_error_row_Combined['delta max'] = pd.to_numeric(max_error_row_Combined['delta max'], errors='coerce')
            max_error_row_Combined['uncertainty'] = pd.to_numeric(max_error_row_Combined['uncertainty'], errors='coerce')
            # Ensure that the following columns are numeric for format output
            mean_error_row_Combined['DCF_Max'] = pd.to_numeric(mean_error_row_Combined['DCF_Max'], errors='coerce')
            mean_error_row_Combined['DCFERR'] = pd.to_numeric(mean_error_row_Combined['DCFERR'], errors='coerce')
            mean_error_row_Combined['EstimatedDelay'] = pd.to_numeric(mean_error_row_Combined['EstimatedDelay'],  errors='coerce')
            mean_error_row_Combined['bin'] = pd.to_numeric(mean_error_row_Combined['bin'], errors='coerce')
            mean_error_row_Combined['delta min'] = pd.to_numeric(mean_error_row_Combined['delta min'], errors='coerce')
            mean_error_row_Combined['delta max'] = pd.to_numeric(mean_error_row_Combined['delta max'], errors='coerce')
            mean_error_row_Combined['uncertainty'] = pd.to_numeric(mean_error_row_Combined['uncertainty'], errors='coerce')
            # Ensure that the following columns are numeric for format output
            last_error_mode_row_Combined['DCF_Max'] = pd.to_numeric(last_error_mode_row_Combined['DCF_Max'], errors='coerce')
            last_error_mode_row_Combined['DCFERR'] = pd.to_numeric(last_error_mode_row_Combined['DCFERR'], errors='coerce')
            last_error_mode_row_Combined['EstimatedDelay'] = pd.to_numeric(
                last_error_mode_row_Combined['EstimatedDelay'], errors='coerce')
            last_error_mode_row_Combined['bin'] = pd.to_numeric(last_error_mode_row_Combined['bin'], errors='coerce')
            last_error_mode_row_Combined['delta min'] = pd.to_numeric(last_error_mode_row_Combined['delta min'], errors='coerce')
            last_error_mode_row_Combined['delta max'] = pd.to_numeric(last_error_mode_row_Combined['delta max'], errors='coerce')
            last_error_mode_row_Combined['uncertainty'] = pd.to_numeric(last_error_mode_row_Combined['uncertainty'], errors='coerce')
                                    # Convert each DataFrame into a Series by selecting the first row
            max_error_antepenultimate = max_error_row_Combined.iloc[0]
            mean_error_penultimate = mean_error_row_Combined.iloc[0]
            last_error_mode_last = last_error_mode_row_Combined.iloc[0]
                                    # Call function for displaying results with a search range
            outputResults_DCF.display_dcf_results_searchRange(frameResults, max_error_antepenultimate, mean_error_penultimate, last_error_mode_last)
            # The next code is for creating a csv file for output
            # Define the format for numeric columns
            qty_decimals = '{:.4f}'  # Choosed the number of four decimal places
            # Apply formatting to specific numeric columns
            floating_columns = ['DCF_Max', 'DCFERR', 'EstimatedDelay', 'bin', 'delta min', 'delta max', 'uncertainty']
            DCF_CFcycle_Data[floating_columns] = DCF_CFcycle_Data[floating_columns].applymap(lambda x: qty_decimals.format(x))
            DCF_CFtrend_Data[floating_columns] = DCF_CFtrend_Data[floating_columns].applymap(lambda x: qty_decimals.format(x))
            ##
            max_error_row_Combined[floating_columns] = max_error_row_Combined[floating_columns].applymap(lambda x: qty_decimals.format(x))
            mean_error_row_Combined[floating_columns] = mean_error_row_Combined[floating_columns].applymap(lambda x: qty_decimals.format(x))
            last_error_mode_row_Combined[floating_columns] = last_error_mode_row_Combined[floating_columns].applymap(lambda x: qty_decimals.format(x))
            # first concataneion of the dataframes
            combined_df_A = pd.concat([DCF_CFtrend_Data, header1, DCF_CFcycle_Data, header1], ignore_index=True)
            # concatanate the last four rows of the file
            combined_df_B = max_error_row_Combined.append([mean_error_row_Combined, last_error_mode_row_Combined], ignore_index=True)
            # second concatenation
            combined_df_DCF_SR = pd.concat([combined_df_A, combined_df_B], ignore_index=True)
            # convert the dataframes concateneted to an output file in csv
            #combined_df_C.to_csv("resultsDCF_CF_cycle_trend_SearchRange.csv", header=True, index=True)
            banderaKnownDelay = 0

    elif preprocessing_selectionAA == 'Wavelet Denoise lvl 1' and delayMethod_selectionAA == 'Discrete Correlation Function (DCF)':
        prep_technique = "WDlvl1"
        level = 1
        if banderaKnownDelay == 1:
            df_lcA_wd1, df_lcB_wd1 = waveletDenoise_function.waveletDenoise(dfA, dfB, hint_delay, level)

            DCF_WD1_KD = function_dcf_EK.find_dcf_delay(df_lcA_wd1, df_lcB_wd1, hint_delay, prep_technique)
            #
            DCF_WD1_KD['DCF_Max'] = pd.to_numeric(DCF_WD1_KD['DCF_Max'], errors='coerce')
            DCF_WD1_KD['DCFERR'] = pd.to_numeric(DCF_WD1_KD['DCFERR'], errors='coerce')
            DCF_WD1_KD['EstimatedDelay'] = pd.to_numeric(DCF_WD1_KD['EstimatedDelay'], errors='coerce')
            DCF_WD1_KD['bin'] = pd.to_numeric(DCF_WD1_KD['bin'], errors='coerce')
            DCF_WD1_KD['delta min'] = pd.to_numeric(DCF_WD1_KD['delta min'], errors='coerce')
            DCF_WD1_KD['delta max'] = pd.to_numeric(DCF_WD1_KD['delta max'], errors='coerce')
            DCF_WD1_KD['uncertainty'] = pd.to_numeric(DCF_WD1_KD['uncertainty'], errors='coerce')
            DCF_WD1_KD['error'] = pd.to_numeric(DCF_WD1_KD['error'], errors='coerce')

            #DCF_WD1.to_csv("resultsDCF_WDlvl1_KnownDelay.csv", index=True, header=True)
            last_four_rows = DCF_WD1_KD.iloc[-4:]
            row1_preantepenultimate = last_four_rows.iloc[0]  # get first row
            row2_antepenultimate = last_four_rows.iloc[1]  # get second row
            row3_penultimate = last_four_rows.iloc[2]  # get third row
            row4_last = last_four_rows.iloc[3]  # get fourth row
                        # Call function to display the output resultswith a known delay
            outputResults_DCF.display_dcf_results_knownDelay(frameResults, row1_preantepenultimate, row2_antepenultimate, row3_penultimate, row4_last)
            banderaSearchRange = 0
        elif banderaSearchRange == 1:
            df_lcA_wd1, df_lcB_wd1 = waveletDenoise_function.waveletDenoise(dfA, dfB, hint_delay, level)
            DCF_WD1_SR = function_dcf_EK.find_dcf_delay(df_lcA_wd1, df_lcB_wd1, hint_delay, prep_technique)
            #
            DCF_WD1_SR['DCF_Max'] = pd.to_numeric(DCF_WD1_SR['DCF_Max'], errors='coerce')
            DCF_WD1_SR['DCFERR'] = pd.to_numeric(DCF_WD1_SR['DCFERR'], errors='coerce')
            DCF_WD1_SR['EstimatedDelay'] = pd.to_numeric(DCF_WD1_SR['EstimatedDelay'], errors='coerce')
            DCF_WD1_SR['bin'] = pd.to_numeric(DCF_WD1_SR['bin'], errors='coerce')
            DCF_WD1_SR['delta min'] = pd.to_numeric(DCF_WD1_SR['delta min'], errors='coerce')
            DCF_WD1_SR['delta max'] = pd.to_numeric(DCF_WD1_SR['delta max'], errors='coerce')
            DCF_WD1_SR['uncertainty'] = pd.to_numeric(DCF_WD1_SR['uncertainty'], errors='coerce')
            DCF_WD1_SR['error'] = pd.to_numeric(DCF_WD1_SR['error'], errors='coerce')

            DCF_WD1_SR.columns = ['DCF_Max', 'DCFERR', 'EstimatedDelay', 'bin', 'delta min', 'delta max', 'search range',
                               'prep_technique', 'error', 'uncertainty']
            DCF_WD1_SR.drop('error', axis=1, inplace=True)
            DCF_WD1_SR.drop(DCF_WD1_SR.index[-4], axis=0, inplace=True)
            # Insert search range
            DCF_WD1_SR['search range'] = DCF_WD1_SR['search range'].apply(lambda x: str(input_valueCombobox))
            #DCF_WD1_SR.to_csv("resultsDCF_WDlvl1_SearchRange.csv", index=True, header=True)
            # prepare DCF_WD1 output
            last_three_rows = DCF_WD1_SR.iloc[-3:]
            row_1_antepenultimate = last_three_rows.iloc[0]  # get first row
            row_2_penultimate = last_three_rows.iloc[1]  # get second row
            row_3_last = last_three_rows.iloc[2]  # get third row
                        # Call function for displaying results with a search range
            outputResults_DCF.display_dcf_results_searchRange(frameResults, row_1_antepenultimate, row_2_penultimate, row_3_last)
            banderaKnownDelay = 0
         # Next option DCF and WD2
    elif preprocessing_selectionAA == 'Wavelet Denoise lvl 2' and delayMethod_selectionAA == 'Discrete Correlation Function (DCF)':
        prep_technique = "WDlvl2"

        if banderaKnownDelay == 1:
            level = 2
            df_lcA_wd2, df_lcB_wd2 = waveletDenoise_function.waveletDenoise(dfA, dfB, hint_delay, level)

            DCF_WD2_KD = function_dcf_EK.find_dcf_delay(df_lcA_wd2, df_lcB_wd2, hint_delay, prep_technique)
            #
            DCF_WD2_KD['DCF_Max'] = pd.to_numeric(DCF_WD2_KD['DCF_Max'], errors='coerce')
            DCF_WD2_KD['DCFERR'] = pd.to_numeric(DCF_WD2_KD['DCFERR'], errors='coerce')
            DCF_WD2_KD['EstimatedDelay'] = pd.to_numeric(DCF_WD2_KD['EstimatedDelay'], errors='coerce')
            DCF_WD2_KD['bin'] = pd.to_numeric(DCF_WD2_KD['bin'], errors='coerce')
            DCF_WD2_KD['delta min'] = pd.to_numeric(DCF_WD2_KD['delta min'], errors='coerce')
            DCF_WD2_KD['delta max'] = pd.to_numeric(DCF_WD2_KD['delta max'], errors='coerce')
            DCF_WD2_KD['uncertainty'] = pd.to_numeric(DCF_WD2_KD['uncertainty'], errors='coerce')
            DCF_WD2_KD['error'] = pd.to_numeric(DCF_WD2_KD['error'], errors='coerce')

            #DCF_WD2.to_csv("resultsDCF_WDlvl2_KnownDelay.csv", index=True, header=True)
            last_four_rows = DCF_WD2_KD.iloc[-4:]
            #result_text.delete(1.0, tk.END)
            row1_preantepenultimate = last_four_rows.iloc[0]  # get first row
            row2_antepenultimate = last_four_rows.iloc[1]  # get second row
            row3_penultimate = last_four_rows.iloc[2]  # get third row
            row4_last = last_four_rows.iloc[3]  # get fourth row
            # Call function to display the output results with a known delay
            outputResults_DCF.display_dcf_results_knownDelay(frameResults, row1_preantepenultimate, row2_antepenultimate, row3_penultimate, row4_last)
            banderaSearchRange = 0
        elif banderaSearchRange == 1:
            level = 2
            df_lcA_wd2, df_lcB_wd2 = waveletDenoise_function.waveletDenoise(dfA, dfB, hint_delay, level)

            DCF_WD2_SR = function_dcf_EK.find_dcf_delay(df_lcA_wd2, df_lcB_wd2, hint_delay, prep_technique)
            #
            DCF_WD2_SR['DCF_Max'] = pd.to_numeric(DCF_WD2_SR['DCF_Max'], errors='coerce')
            DCF_WD2_SR['DCFERR'] = pd.to_numeric(DCF_WD2_SR['DCFERR'], errors='coerce')
            DCF_WD2_SR['EstimatedDelay'] = pd.to_numeric(DCF_WD2_SR['EstimatedDelay'], errors='coerce')
            DCF_WD2_SR['bin'] = pd.to_numeric(DCF_WD2_SR['bin'], errors='coerce')
            DCF_WD2_SR['delta min'] = pd.to_numeric(DCF_WD2_SR['delta min'], errors='coerce')
            DCF_WD2_SR['delta max'] = pd.to_numeric(DCF_WD2_SR['delta max'], errors='coerce')
            DCF_WD2_SR['uncertainty'] = pd.to_numeric(DCF_WD2_SR['uncertainty'], errors='coerce')
            DCF_WD2_SR['error'] = pd.to_numeric(DCF_WD2_SR['error'], errors='coerce')

            DCF_WD2_SR.columns = ['DCF_Max', 'DCFERR', 'EstimatedDelay', 'bin', 'delta min', 'delta max', 'search range',
                               'prep_technique', 'error', 'uncertainty']
            DCF_WD2_SR.drop('error', axis=1, inplace=True)
            DCF_WD2_SR.drop(DCF_WD2_SR.index[-4], axis=0, inplace=True)
            # Insert search range
            DCF_WD2_SR['search range'] = DCF_WD2_SR['search range'].apply(lambda x: str(input_valueCombobox))
            #DCF_WD2.to_csv("resultsDCF_WDlvl2_SearchRange.csv", index=True, header=True)
            # prepare DCF_WD1 output
            last_three_rows = DCF_WD2_SR.iloc[-3:]
            row_1_antepenultimate = last_three_rows.iloc[0]  # get first row
            row_2_penultimate = last_three_rows.iloc[1]  # get second row
            row_3_last = last_three_rows.iloc[2]  # get third row
                        # Call function for displaying results with a search range
            outputResults_DCF.display_dcf_results_searchRange(frameResults, row_1_antepenultimate, row_2_penultimate, row_3_last)
            banderaKnownDelay = 0
         # Option DCF and WD3
    elif preprocessing_selectionAA == 'Wavelet Denoise lvl 3' and delayMethod_selectionAA == 'Discrete Correlation Function (DCF)':
        prep_technique = "WDlvl3"
        level = 3

        if banderaKnownDelay == 1:

            df_lcA_wd3, df_lcB_wd3 = waveletDenoise_function.waveletDenoise(dfA, dfB, hint_delay, level)

            DCF_WD3_KD = function_dcf_EK.find_dcf_delay(df_lcA_wd3, df_lcB_wd3, hint_delay, prep_technique)
            #
            DCF_WD3_KD['DCF_Max'] = pd.to_numeric(DCF_WD3_KD['DCF_Max'], errors='coerce')
            DCF_WD3_KD['DCFERR'] = pd.to_numeric(DCF_WD3_KD['DCFERR'], errors='coerce')
            DCF_WD3_KD['EstimatedDelay'] = pd.to_numeric(DCF_WD3_KD['EstimatedDelay'], errors='coerce')
            DCF_WD3_KD['bin'] = pd.to_numeric(DCF_WD3_KD['bin'], errors='coerce')
            DCF_WD3_KD['delta min'] = pd.to_numeric(DCF_WD3_KD['delta min'], errors='coerce')
            DCF_WD3_KD['delta max'] = pd.to_numeric(DCF_WD3_KD['delta max'], errors='coerce')
            DCF_WD3_KD['uncertainty'] = pd.to_numeric(DCF_WD3_KD['uncertainty'], errors='coerce')
            DCF_WD3_KD['error'] = pd.to_numeric(DCF_WD3_KD['error'], errors='coerce')

            #DCF_WD3.to_csv("resultsDCF_WDlvl3_KnownDelay.csv", index=True, header=True)
            last_four_rows = DCF_WD3_KD.iloc[-4:]
            row1_preantepenultimate = last_four_rows.iloc[0]  # get first row
            row2_antepenultimate = last_four_rows.iloc[1]  # get second row
            row3_penultimate = last_four_rows.iloc[2]  # get third row
            row4_last = last_four_rows.iloc[3]  # get fourth row
            # Call function to display the output results with a known delay
            outputResults_DCF.display_dcf_results_knownDelay(frameResults, row1_preantepenultimate, row2_antepenultimate, row3_penultimate, row4_last)
            banderaSearchRange = 0
        elif banderaSearchRange == 1:
            # Call function for denoising the light curves A and B
            df_lcA_wd3, df_lcB_wd3 = waveletDenoise_function.waveletDenoise(dfA, dfB, hint_delay, level)

            DCF_WD3_SR = function_dcf_EK.find_dcf_delay(df_lcA_wd3, df_lcB_wd3, hint_delay, prep_technique)
            #
            DCF_WD3_SR['DCF_Max'] = pd.to_numeric(DCF_WD3_SR['DCF_Max'], errors='coerce')
            DCF_WD3_SR['DCFERR'] = pd.to_numeric(DCF_WD3_SR['DCFERR'], errors='coerce')
            DCF_WD3_SR['EstimatedDelay'] = pd.to_numeric(DCF_WD3_SR['EstimatedDelay'], errors='coerce')
            DCF_WD3_SR['bin'] = pd.to_numeric(DCF_WD3_SR['bin'], errors='coerce')
            DCF_WD3_SR['delta min'] = pd.to_numeric(DCF_WD3_SR['delta min'], errors='coerce')
            DCF_WD3_SR['delta max'] = pd.to_numeric(DCF_WD3_SR['delta max'], errors='coerce')
            DCF_WD3_SR['uncertainty'] = pd.to_numeric(DCF_WD3_SR['uncertainty'], errors='coerce')
            DCF_WD3_SR['error'] = pd.to_numeric(DCF_WD3_SR['error'], errors='coerce')

            DCF_WD3_SR.columns = ['DCF_Max', 'DCFERR', 'EstimatedDelay', 'bin', 'delta min', 'delta max', 'search range',
                               'prep_technique', 'error', 'uncertainty']
            DCF_WD3_SR.drop('error', axis=1, inplace=True)
            DCF_WD3_SR.drop(DCF_WD3_SR.index[-4], axis=0, inplace=True)
            # Insert search range
            DCF_WD3_SR['search range'] = DCF_WD3_SR['search range'].apply(lambda x: str(input_valueCombobox))
            #DCF_WD3_SR.to_csv("resultsDCF_WDlvl3_SearchRange.csv", index=True, header=True)
            # prepare DCF_WD1 output
            last_three_rows = DCF_WD3_SR.iloc[-3:]
            row_1_antepenultimate = last_three_rows.iloc[0]  # get first row
            row_2_penultimate = last_three_rows.iloc[1]  # get second row
            row_3_last = last_three_rows.iloc[2]  # get third row
                        # Call function for displaying results with a search range
            outputResults_DCF.display_dcf_results_searchRange(frameResults, row_1_antepenultimate, row_2_penultimate, row_3_last)
            banderaKnownDelay = 0
    else:
        pass

def display_statistical_analysis():
    """
    Generates and displays statistical analysis of the uploaded light curves in the GUI, 
    including histograms for raw data and processed data according to the selected preprocessing method.

    This function checks the availability of light curve data and the selected preprocessing method, then generates histograms and descriptive statistics for each light curve. These analyses are displayed in dedicated frames within the application's GUI.

    Global Variables:
    - frameStatistical_A (tk.Frame): Frame for displaying the statistical analysis and histogram of the lead light curve.
    - frameStatistical_B (tk.Frame): Frame for displaying the statistical analysis and histogram of the delayed light curve.
    - canvasSecond (tk.Canvas): Canvas used for plotting histograms in the GUI.
    - initial_canvas (tk.Canvas): Initial canvas displayed at the start of the application, referenced to avoid overlaps with statistical plots.

    Workflow:
    1. Validates the existence of light curve data and the selected preprocessing method.
    2. Clears previous statistical analysis frames to prevent overlap.
    3. Generates histograms for raw and processed light curves depending on the preprocessing selection.
    4. Displays histograms and descriptive statistics within the GUI.

    Note:
    - This function is dependent on the global `series_data` variable that stores the uploaded light curve data.
    - The actual plotting is done using matplotlib, and the plots are integrated into the Tkinter GUI via the FigureCanvasTkAgg widget.
    """
    if series_data[1] is None or series_data[2] is None:
        return
    preprocessing_selectionSA = preprocessing_selection.get()
    if preprocessing_selectionSA is None:
       return
    if preprocessing_selectionSA == 'Select item':
       return
    global frameStatistical_A  # Reference the global_frame variable
    global frameStatistical_B  # Reference the global_frame variable
    global canvasSecond
    global initial_canvas
    global export_button
    # declare variables for CF-filter
    global figCFcycle_A
    global figCFcycle_B
    global formatted_output_lead_CF_cycle
    global formatted_output_delayed_CF_cycle
    global figCFtrend_A
    global figCFtrend_B
    global formatted_output_lead_CF_trend
    global formatted_output_delayed_CF_trend
    global figCF
    # Call function to clear the frame of the initial figure
    clear_frame(framePlot_lcAB)
    # Clear content in every function call for the statistical analysis output frames
    if frameStatistical_A is not None:
        frame_clear.clear_frame(frameStatistical_A)
    if frameStatistical_B is not None:
        frame_clear.clear_frame(frameStatistical_B)

    if preprocessing_selectionSA == 'Raw Data':
        # Remove the frame and canvas from the grid layout
        if frameStatistical_A:
            frameStatistical_A.grid_forget()
        if frameStatistical_B:
            frameStatistical_B.grid_forget()

        lc_Araw = series_data[1].copy()
        lc_Braw = series_data[2].copy()
        lc_Araw.rename(columns={"Julian_day": "timeRaw", "Magnitude": "lc_A_raw", "error": "error_Araw"}, inplace=True)
        lc_Araw['pctError_A_raw'] = lc_Araw['error_Araw'] / lc_Araw['lc_A_raw']
        lc_Braw.rename(columns={"Julian_day": "timeRaw", "Magnitude": "lc_B_raw", "error": "error_Braw"}, inplace=True)
        lc_Braw['pctError_B_raw'] = lc_Braw['error_Braw'] / lc_Braw['lc_B_raw']

        figRawA = plt.Figure(figsize=(2.5, 1.95))
        lc_A_raw_hst = figRawA.add_subplot(111)

        figRawB = plt.Figure(figsize=(2.5, 1.95))
        lc_B_raw_hst = figRawB.add_subplot(111)
        # Create both histograms
        lc_A_raw_hst.hist(lc_Araw['lc_A_raw'], bins=10, alpha=0.5, color="blue", ec="black", lw=3)
        lc_A_raw_hst.set_title("Lead light curve in raw data", fontsize=8)  # Add title to histogram
        #set size for ticks labels for light curve A
        lc_A_raw_hst.tick_params(axis="x", labelsize=6)
        lc_A_raw_hst.tick_params(axis="y", labelsize=6)
        lc_B_raw_hst.hist(lc_Braw['lc_B_raw'], bins=10, alpha=0.5, color="#8B7B8B", ec="black", lw=3)  # thistle4  #8B7B8B  RGB(139,123,139)
        lc_B_raw_hst.set_title("Delayed light curve in raw data", fontsize=8)  # Add title to histogram
        #set size for ticks labels for light curve B
        lc_B_raw_hst.tick_params(axis="x", labelsize=6)
        lc_B_raw_hst.tick_params(axis="y", labelsize=6)
        # Create a Frame to hold the widgets
        frameStatistical_A = tk.Frame(root)
        frameStatistical_B = tk.Frame(root)
        frameStatistical_A.grid(row=1, column=1, padx=3, pady=3)
        frameStatistical_B.grid(row=2, column=1, padx=3, pady=3)

        canvasRawA = FigureCanvasTkAgg(figRawA, master=frameStatistical_A)
        canvasRawB = FigureCanvasTkAgg(figRawB, master=frameStatistical_B)
        canvas_widgetRawA = canvasRawA.get_tk_widget()
        canvas_widgetRawB = canvasRawB.get_tk_widget()

        canvas_widgetRawA.grid(row=0, column=0, columnspan=2)
        canvas_widgetRawB.grid(row=0, column=0, columnspan=2)
        # Adjust the Canvas widget's size to make the figure smaller
        statisticalAnalysisA = tk.Text(frameStatistical_A, width=26, height=17, bg="#00CDCD",
                                       font=("Courier", 10))  # cyan3	#00CDCD	RGB(0,205,205)
        statisticalAnalysisA.grid(row=0, column=3, columnspan=1, padx=2, pady=2)

        statisticalAnalysisB = tk.Text(frameStatistical_B, width=26, height=17, bg="#7EC0EE",
                                       font=("Courier", 10))  # skyblue2 #7EC0EE RGB(126,192,238)
        statisticalAnalysisB.grid(row=0, column=3, columnspan=1, padx=2, pady=2)
        # Adjust the figsize to decrease the size of the graphic
        figRawlc = plt.Figure(figsize=(4.7, 2.65))
        ax = figRawlc.add_subplot(111)
        # ax.set_position is [left, bottom, width, height] by increasing the third an fourth parameter
        # the plot looks tighter
        ax.set_position([0.14, 0.1585, 0.85, 0.83])
        ########################################
        # We have two light curves in series_data named 1 and 2
        df_A = series_data[1].copy()
        df_B = series_data[2].copy()
        # Calculate the pct error of each curve
        time = df_A['time']
        # calculate the percentage error
        pct_err_A = df_A['error'] / df_A['Magnitude']
        pct_err_B = df_B['error'] / df_B['Magnitude']
        # Realizar la estandarización de las series de tiempo
        scalerA = MinMaxScaler(feature_range=(0.15, 0.25))
        scalerB = MinMaxScaler(feature_range=(0.1, 0.2))

        df_A['Magnitude'] = scalerA.fit_transform(df_A['Magnitude'].values.reshape(-1, 1)).flatten()
        df_B['Magnitude'] = scalerB.fit_transform(df_B['Magnitude'].values.reshape(-1, 1)).flatten()
        # recalculate the error with standarized data
        err_A = abs(df_A['Magnitude'] * pct_err_A)
        err_B = abs(df_B['Magnitude'] * pct_err_B)

        lightCurve_A = {
            'time': time,
            'lc_A': df_A['Magnitude'],
            'err_A': err_A,}
        lightCurve_B = {
            'time': time,
            'lc_B': df_B['Magnitude'],
            'err_B': err_B,}
        # Plot the first DataFrame
        ax.errorbar(lightCurve_A['time'], lightCurve_A['lc_A'], yerr=lightCurve_A['err_A'], fmt='s', elinewidth=0.5,
                    markersize=1, label="Lead light curve")
        # Plot the second DataFrame
        ax.errorbar(lightCurve_B['time'], lightCurve_B['lc_B'], yerr=lightCurve_B['err_B'], fmt='s', elinewidth=0.5,
                    markersize=1, label="Delayed light curve")
        ax.set_xlabel("Time (days)", fontsize=8)
        ax.set_ylabel("lead lc offset 0.15, delayed lc offset 0.1\nMagnitude", fontsize=6)
        ax.tick_params(axis="x", labelsize=6)
        ax.tick_params(axis="y", labelsize=6)
        ax.legend()
        ###########################################
        initial_canvas = FigureCanvasTkAgg(figRawlc, master=framePlot_lcAB)
        canvas_widget = initial_canvas.get_tk_widget()
        canvas_widget.grid(row=0, column=0, columnspan=1)
        # Begin the descriptive statistics to the initial raw data apply the different techniques light curve A
        lcA_Raw = lc_Araw['lc_A_raw']
        Hurst, c, data = compute_Hc(lcA_Raw, kind='random_walk', simplified=True)
        skewness = skew(lcA_Raw, axis=0, bias=True)
        curtosis = kurtosis(lcA_Raw, axis=0, fisher=False, bias=True)
        resA, resB = stats.jarque_bera(lcA_Raw)
        resultA = adfuller(lcA_Raw)
        adfStatistic = resultA[0]
        adfPvalue = resultA[1]
        # Extract and print the critical values in a dictionary
        critical_values_dict = {key: value for key, value in resultA[4].items()}
        first_critical_valueA = critical_values_dict['1%']
        second_critical_valueA = critical_values_dict['5%']
        third_critical_valueA = critical_values_dict['10%']
        empty = ""
        statsA = {
            'count': lcA_Raw.count(),
            'mean': lcA_Raw.mean(),
            'std.dev': lcA_Raw.std(),
            'min': lcA_Raw.min(),
            'max': lcA_Raw.max(),
            'Hurst': Hurst,
            'Skewness': skewness,
            'Kurtosis': curtosis,
            'Jarque-Bera': resA,
            'P-value': resB,
            'ADF-Statistic': adfStatistic,
            'p-value': adfPvalue,
            'Critical-Vals': empty,
            '1%:': first_critical_valueA,
            '5%:': second_critical_valueA,
            '10%:': third_critical_valueA }
        # Create a DataFrame with a single-row index
        df_statsA = pd.DataFrame(statsA, index=['Statistics'])
        # Transpose the DataFrame
        df_statsA_transposed = df_statsA.transpose()
        # Convert the data in the second column to numeric and apply formatting-for only two decimal points
        column_name = 'Statistics'
        df_statsA_transposed[column_name] = pd.to_numeric(df_statsA_transposed[column_name], errors='coerce').apply(
            lambda x: f'{x:.2f}' if not pd.isnull(x) else '')
        # Get the formatted DataFrame as a string without the header and index
        statsA_str = df_statsA_transposed.to_string(header=False, index=False)
        # Create a list of lines with both column names and values
        lines = [f'{col:<18}{val}' if val else f'{col}' for col, val in
                 zip(df_statsA_transposed.index, statsA_str.split('\n'))]
        # Insert lines into the Text widget with line breaks
        formatted_output_rawlead = '\n'.join(lines)
        statisticalAnalysisA.insert(tk.END, formatted_output_rawlead)
        # Begin the descriptive statistics to the initial raw data apply the different techniques light curve B
        lcB_Raw = lc_Braw['lc_B_raw']
        HurstB, c, data = compute_Hc(lcB_Raw, kind='random_walk', simplified=True)
        skewnessB = skew(lcB_Raw, axis=0, bias=True)
        curtosisB = kurtosis(lcB_Raw, axis=0, fisher=False, bias=True)  # Pearson kurtosis normal distribution = 3
        resC, resD = stats.jarque_bera(lcB_Raw)
        resultB = adfuller(lcB_Raw)
        adfStatisticB = resultB[0]
        adfPvalueB = resultB[1]
        # Extract and print the critical values in a dictionary
        critical_values_dictB = {key: value for key, value in resultB[4].items()}
        first_critical_valueB = critical_values_dictB['1%']
        second_critical_valueB = critical_values_dictB['5%']
        third_critical_valueB = critical_values_dictB['10%']
        emptyB = ""
        statsB = {
            'count': lcB_Raw.count(),
            'mean': lcB_Raw.mean(),
            'std.dev': lcB_Raw.std(),
            'min': lcB_Raw.min(),
            'max': lcB_Raw.max(),
            'Hurst': HurstB,
            'Skewness': skewnessB,
            'Kurtosis': curtosisB,
            'Jarque-Bera': resC,
            'P-value': resD,
            'ADF-Statistic': adfStatisticB,
            'p-value': adfPvalueB,
            'Critical-Vals': emptyB,
            '1%:': first_critical_valueB,
            '5%:': second_critical_valueB,
            '10%:': third_critical_valueB   }
        # Create light curve B  DataFrame with a single-row index
        df_statsB = pd.DataFrame(statsB, index=['Statistics'])
        # Transpose the DataFrame
        df_statsB_transposed = df_statsB.transpose()
        # Convert the data in the second column to numeric and apply formatting-for only two decimal points
        column_nameB = 'Statistics'
        df_statsB_transposed[column_nameB] = pd.to_numeric(df_statsB_transposed[column_name], errors='coerce').apply(
            lambda x: f'{x:.2f}' if not pd.isnull(x) else '')
        # Get the formatted DataFrame as a string without the header and index
        statsB_str = df_statsB_transposed.to_string(header=False, index=False)
        # Create a list of lines with both column names and values
        linesB = [f'{col:<18}{val}' if val else f'{col}' for col, val in
                  zip(df_statsB_transposed.index, statsB_str.split('\n'))]
        # Insert lines into the Text widget with line breaks
        formatted_output_rawdelay = '\n'.join(linesB)
        statisticalAnalysisB.insert(tk.END, formatted_output_rawdelay)
        # restart preprocessing_selectionSA value
        preprocessing_selectionSA = 'Select item'
                                # Call function to output pdf file
        colour1 = '#020f12'
        colour2 = '#DCDCDC'
        colour3 = '#C1CDC1'
        colour4 = '#292421'
        export_button = tk.Button(root, background=colour2, foreground=colour4, activebackground=colour3,
                           activeforeground=colour4, highlightthickness=4, highlightbackground=colour2,
                           highlightcolor='BLUE', width=28, height=1, border=2, cursor='hand1', font=('Arial', 13, 'bold'), text="Export descriptive statistics to PDF",
                           command =lambda: export_histogram_and_stats_to_pdf(
                           figures=[figRawA, figRawB],
                           stats_data=[formatted_output_rawlead, formatted_output_rawdelay],
                           headers=['Descriptive Statistics for Lead Light Curve with Raw Data', 'Descriptive Statistics for Delayed Light Curve with Raw Data'],
                           additional_figure=figRawlc,
                           additional_header="Light Curves with Raw Data",
                           initial_dir =os.path.expanduser('~'),
                           initial_file ="Plot_and_Statistics_Raw_Data.pdf"
                           ))
        export_button.grid(row=0, column=1, pady=10)
    elif preprocessing_selectionSA == 'Data Differencing':
        # Remove the frame and canvas from the grid layout
        if frameStatistical_A:
            frameStatistical_A.grid_forget()
        if frameStatistical_B:
            frameStatistical_B.grid_forget()
        if export_button:
             export_button.destroy()
            #
        lc_Adiff = series_data[1].copy()
        lc_Bdiff = series_data[2].copy()
        lc_Adiff.rename(columns={"Julian_day": "timeDiff", "Magnitude": "lc_A_diff", "error": "error_A_diff"}, inplace=True)
        lc_Adiff['pctError_A_diff'] = lc_Adiff['error_A_diff'] / lc_Adiff['lc_A_diff']
        lc_Bdiff.rename(columns={"Julian_day": "timeDiff", "Magnitude": "lc_B_diff", "error": "error_B_diff"}, inplace=True)
        lc_Bdiff['pctError_B_diff'] = lc_Bdiff['error_B_diff'] / lc_Bdiff['lc_B_diff']
        time_diff = lc_Adiff['time']
        time_diff = time_diff.tail(-1)
        differenced_mag_A = lc_Adiff['lc_A_diff'].diff()
        differenced_mag_B = lc_Bdiff['lc_B_diff'].diff()

        diff_magerr_A = abs(differenced_mag_A * lc_Adiff['pctError_A_diff'])
        diff_magerr_B = abs(differenced_mag_B * lc_Bdiff['pctError_B_diff'])

        differenced_mag_A = pd.Series(differenced_mag_A).tail(-1)
        diff_magerr_A = pd.Series(diff_magerr_A).tail(-1)
        differenced_mag_B = pd.Series(differenced_mag_B).tail(-1)
        diff_magerr_B = pd.Series(diff_magerr_B).tail(-1)

        lightCurve_A_diff = {
            'time_diff': time_diff,
            'differenced_mag_A': differenced_mag_A,
            'diff_magerr_A': diff_magerr_A,  }
        lightCurve_B_diff = {
            'time_diff': time_diff,
            'differenced_mag_B': differenced_mag_B,
            'diff_magerr_B': diff_magerr_B }
        # Plot the differenced data in a histogram
        figDiffA = plt.Figure(figsize=(2.5, 1.95))
        lcAdiff_hst = figDiffA.add_subplot(111)
        lcAdiff_hst.hist(lightCurve_A_diff['differenced_mag_A'], bins=10, alpha=0.5, color="blue", ec="black", lw=3)
        lcAdiff_hst.set_title("Lead light curve with differencing", fontsize=8)  # Add title to histogram A
        #set size for ticks labels for light curve A
        lcAdiff_hst.tick_params(axis="x", labelsize=6)
        lcAdiff_hst.tick_params(axis="y", labelsize=6)
        figDiffB = plt.Figure(figsize=(2.5, 1.95))
        lcBdiff_hst = figDiffB.add_subplot(111)
        lcBdiff_hst.hist(lightCurve_B_diff['differenced_mag_B'], bins=10, alpha=0.5, color="#8B7B8B", ec="black", lw=3)  # 8B7B8B
        lcBdiff_hst.set_title("Delayed light curve with differencing", fontsize=8)  # Add title to histogram A
        lcBdiff_hst.tick_params(axis="x", labelsize=6)
        lcBdiff_hst.tick_params(axis="y", labelsize=6)
        # Create a Frame to hold the widgets
        frameStatistical_A = tk.Frame(root)
        frameStatistical_B = tk.Frame(root)
        frameStatistical_A.grid(row=1, column=1, padx=3, pady=3)
        frameStatistical_B.grid(row=2, column=1, padx=3, pady=3)

        canvasdiffA = FigureCanvasTkAgg(figDiffA, master=frameStatistical_A)
        canvasdiffB = FigureCanvasTkAgg(figDiffB, master=frameStatistical_B)
        canvas_widgetDiffA = canvasdiffA.get_tk_widget()
        canvas_widgetDiffA.grid(row=0, column=0, columnspan=2)

        canvas_widgetDiffB = canvasdiffB.get_tk_widget()
        canvas_widgetDiffB.grid(row=0, column=0, columnspan=2)
        ########################################################################
        # Begin the code for plot the light curves A and B and to adjust the figsize to decrease or increase the size of the graphic
        figDiff = plt.Figure(figsize=(4.7, 2.65))
        axDiff = figDiff.add_subplot(111)
        # ax.set_position is [left, bottom, width, height] by increasing the third an fourth parameter
        # the plot looks tighter
        axDiff.set_position([0.11, 0.1585, 0.85, 0.83])
        # Plot the first DataFrame
        axDiff.errorbar(lightCurve_A_diff['time_diff'], lightCurve_A_diff['differenced_mag_A'],
                        yerr=lightCurve_A_diff['diff_magerr_A'], fmt='s', elinewidth=0.5, markersize=1,
                        label="Lead light curve")
        # Plot the second DataFrame
        axDiff.errorbar(lightCurve_B_diff['time_diff'], lightCurve_B_diff['differenced_mag_B'],
                        yerr=lightCurve_B_diff['diff_magerr_B'], fmt='s', elinewidth=0.5, markersize=1,
                        label="Delayed light curve")
        axDiff.set_xlabel("Time (days)", fontsize=8)
        axDiff.set_ylabel("Magnitude", fontsize=8)
        axDiff.tick_params(axis="x", labelsize=6)
        axDiff.tick_params(axis="y", labelsize=6)
        axDiff.legend()
        initial_canvas = FigureCanvasTkAgg(figDiff, master=framePlot_lcAB)
        canvas_widgetDiff = initial_canvas.get_tk_widget()
        canvas_widgetDiff.grid(row=0, column=0, columnspan=1)
        # Begin the descriptive statistics to the initial raw data apply the different techniques light curve A
        lcA_Diff = differenced_mag_A
        HurstA, c, data = compute_Hc(lcA_Diff, kind='random_walk', simplified=True)
        skewnessA = skew(lcA_Diff, axis=0, bias=True)
        curtosisA = kurtosis(lcA_Diff, axis=0, fisher=False, bias=True)
        resA, resB = stats.jarque_bera(lcA_Diff)
        resultA = adfuller(lcA_Diff)
        adfStatisticA = resultA[0]
        adfPvalueA = resultA[1]
        # Extract and print the critical values in a dictionary
        critical_values_dict = {key: value for key, value in resultA[4].items()}
        first_critical_valueA = critical_values_dict['1%']
        second_critical_valueA = critical_values_dict['5%']
        third_critical_valueA = critical_values_dict['10%']
        empty = ""
        statsA = {
            'count': lcA_Diff.count(),
            'mean': lcA_Diff.mean(),
            'std.dev': lcA_Diff.std(),
            'min': lcA_Diff.min(),
            'max': lcA_Diff.max(),
            'Hurst': HurstA,
            'Skewness': skewnessA,
            'Kurtosis': curtosisA,
            'Jarque-Bera': resA,
            'P-value': resB,
            'ADF-Statistic': adfStatisticA,
            'p-value': adfPvalueA,
            'Critical-Vals': empty,
            '1%:': first_critical_valueA,
            '5%:': second_critical_valueA,
            '10%:': third_critical_valueA
        }
        # Begin the descriptive statistics to the initial raw data apply the different techniques light curve B
        lcB_Diff = differenced_mag_B
        HurstB, c, data = compute_Hc(lcB_Diff, kind='random_walk', simplified=True)
        skewnessB = skew(lcB_Diff, axis=0, bias=True)
        curtosisB = kurtosis(lcB_Diff, axis=0, fisher=False, bias=True)
        resC, resD = stats.jarque_bera(lcB_Diff)
        resultB = adfuller(lcB_Diff)
        adfStatisticB = resultB[0]
        adfPvalueB = resultB[1]
        # Extract and print the critical values in a dictionary
        critical_values_dict = {key: value for key, value in resultA[4].items()}
        first_critical_valueB = critical_values_dict['1%']
        second_critical_valueB = critical_values_dict['5%']
        third_critical_valueB = critical_values_dict['10%']
        statsB = {
            'count': lcB_Diff.count(),
            'mean': lcB_Diff.mean(),
            'std.dev': lcB_Diff.std(),
            'min': lcB_Diff.min(),
            'max': lcB_Diff.max(),
            'Hurst': HurstB,
            'Skewness': skewnessB,
            'Kurtosis': curtosisB,
            'Jarque-Bera': resC,
            'P-value': resD,
            'ADF-Statistic': adfStatisticB,
            'p-value': adfPvalueB,
            'Critical-Vals': empty,
            '1%:': first_critical_valueB,
            '5%:': second_critical_valueB,
            '10%:': third_critical_valueB
        }
        # the descriptive statistic widget
        statisticalAnalysisA = tk.Text(frameStatistical_A, width=26, height=17, bg="#00CDCD",
                                       font=("Courier", 10))  # cyan3	#00CDCD	RGB(0,205,205)
        statisticalAnalysisA.grid(row=0, column=3, columnspan=1, padx=2, pady=2)

        statisticalAnalysisB = tk.Text(frameStatistical_B, width=26, height=17, bg="#7EC0EE",
                                       font=("Courier", 10))  # skyblue2 #7EC0EE RGB(126,192,238)
        statisticalAnalysisB.grid(row=0, column=3, columnspan=1, padx=2, pady=2)

        # Create a DataFrame with a single-row index for light curve A
        df_statsA = pd.DataFrame(statsA, index=['Statistics'])
        # Transpose the DataFrame
        df_statsA_transposed = df_statsA.transpose()
        # Convert the data in the second column to numeric and apply formatting-for only two decimal points
        column_name = 'Statistics'
        df_statsA_transposed[column_name] = pd.to_numeric(df_statsA_transposed[column_name], errors='coerce').apply(
            lambda x: f'{x:.2f}' if not pd.isnull(x) else '')
        # Get the formatted DataFrame as a string without the header and index
        statsA_str = df_statsA_transposed.to_string(header=False, index=False)
        # Create a list of lines with both column names and values
        lines = [f'{col:<18}{val}' if val else f'{col}' for col, val in
                 zip(df_statsA_transposed.index, statsA_str.split('\n'))]
        # Insert lines into the Text widget with line breaks
        formatted_output_Difflead = '\n'.join(lines)
        statisticalAnalysisA.insert(tk.END, formatted_output_Difflead)

        # Create a DataFrame with a single-row index for light curve B
        df_statsB = pd.DataFrame(statsB, index=['Statistics'])
        # Transpose the DataFrame
        df_statsB_transposed = df_statsB.transpose()
        # Convert the data in the second column to numeric and apply formatting-for only two decimal points
        column_nameB = 'Statistics'
        df_statsB_transposed[column_nameB] = pd.to_numeric(df_statsB_transposed[column_nameB], errors='coerce').apply(
            lambda x: f'{x:.2f}' if not pd.isnull(x) else '')
        # Get the formatted DataFrame as a string without the header and index
        statsB_str = df_statsB_transposed.to_string(header=False, index=False)
        # Create a list of lines with both column names and values
        linesB = [f'{col:<18}{val}' if val else f'{col}' for col, val in
                  zip(df_statsB_transposed.index, statsB_str.split('\n'))]
        # Insert lines into the Text widget with line breaks
        formatted_output_Diffdelay = '\n'.join(linesB)
        statisticalAnalysisB.insert(tk.END, formatted_output_Diffdelay)
        plt.show()
        preprocessing_selectionSA = 'Select item'
                        # Call function to output pdf file
        colour1 = '#020f12'
        colour2 = '#DCDCDC'
        colour3 = '#C1CDC1'
        colour4 = '#292421'
        export_button = tk.Button(root, background=colour2, foreground=colour4, activebackground=colour3,
                        activeforeground=colour4, highlightthickness=4, highlightbackground=colour2,
                        highlightcolor='BLUE', width=28, height=1, border=2, cursor='hand1', font=('Arial', 13, 'bold'), text="Export descriptive statistics to PDF",
                        command =lambda: export_histogram_and_stats_to_pdf(
                        figures=[figDiffA, figDiffB],
                        stats_data=[formatted_output_Difflead, formatted_output_Diffdelay],
                        headers=['Descriptive Statistics for Lead Light Curve with Data Differencing', 'Descriptive Statistics for Delayed Light Curve with Data Differencing'],
                        additional_figure=figDiff,
                        additional_header="Light Curves with Data Differencing",
                        initial_dir =os.path.expanduser('~'),
                        initial_file ="Plot_and_Statistics_Data_Differencing.pdf"
                        ))
        export_button.grid(row=0, column=1, pady=10)

    elif preprocessing_selectionSA == 'Simple Net Return':
        # Remove the frame and canvas from the grid layout
        if frameStatistical_A:
            frameStatistical_A.grid_forget()
        if frameStatistical_B:
            frameStatistical_B.grid_forget()
            # Extract required columns
        lc_A_SNR = series_data[1].copy()
        lc_B_SNR = series_data[2].copy()
        lc_A_SNR.rename(columns={"Julian_day": "timeSNR", "Magnitude": "lc_A_SNR", "error": "error_A_SNR"}, inplace=True)
        # dfLights['lcA_pctErr'] = dfLights['lc_AErr'] / dfLights['lc_A']
        lc_A_SNR['pctError_A_SNR'] = lc_A_SNR['error_A_SNR'] / lc_A_SNR['lc_A_SNR']
        lc_B_SNR.rename(columns={"Julian_day": "timeSNR", "Magnitude": "lc_B_SNR", "error": "error_B_SNR"}, inplace=True)
        lc_B_SNR['pctError_B_SNR'] = lc_B_SNR['error_B_SNR'] / lc_B_SNR['lc_B_SNR']
        time_snr = lc_A_SNR['time']
        time_snr = time_snr.tail(-1)
        # Simple Net return (SNR) calculation
        snr_mag_A = lc_A_SNR['lc_A_SNR'].pct_change()
        snr_mag_B = lc_B_SNR['lc_B_SNR'].pct_change()

        error_A_SNR = abs(snr_mag_A * lc_B_SNR['pctError_B_SNR'])
        error_B_SNR = abs(snr_mag_B * lc_B_SNR['pctError_B_SNR'])

        snr_mag_A = pd.Series(snr_mag_A).tail(-1)
        error_A_SNR = pd.Series(error_A_SNR).tail(-1)
        snr_mag_B = pd.Series(snr_mag_B).tail(-1)
        error_B_SNR = pd.Series(error_B_SNR).tail(-1)


        lightCurve_A_SNR = {
            'time_snr': time_snr,
            'snr_mag_A': snr_mag_A,
            'error_A_SNR': error_A_SNR,
        }
        lightCurve_B_SNR = {
            'time_snr': time_snr,
            'snr_mag_B': snr_mag_B,
            'error_B_SNR': error_B_SNR
        }
        # Plot the snr data in an histogram
        figSNR_A = plt.Figure(figsize=(2.5, 1.95))
        lcA_SNR_hst = figSNR_A.add_subplot(111)

        lcA_SNR_hst.hist(lightCurve_A_SNR['snr_mag_A'], bins=10, alpha=0.5, color="blue", ec="black", lw=3)
        lcA_SNR_hst.set_title("Lead light curve in SNR", fontsize=8)  # Add title to histogram A
        lcA_SNR_hst.tick_params(axis="x", labelsize=6)
        lcA_SNR_hst.tick_params(axis="y", labelsize=6)

        figSNR_B = plt.Figure(figsize=(2.5, 1.95))
        lcB_SNR_hst = figSNR_B.add_subplot(111)

        lcB_SNR_hst.hist(lightCurve_B_SNR['snr_mag_B'], bins=10, alpha=0.5, color="#8B7B8B", ec="black", lw=3)  # 8B7B8B
        lcB_SNR_hst.set_title("Delayed light curve in SNR", fontsize=8)  # Add title to histogram A
        lcB_SNR_hst.tick_params(axis="x", labelsize=6)
        lcB_SNR_hst.tick_params(axis="y", labelsize=6)
        # Create a Frame to hold the widgets
        frameStatistical_A = tk.Frame(root)
        frameStatistical_B = tk.Frame(root)

        frameStatistical_A.grid(row=1, column=1, padx=3, pady=3)
        frameStatistical_B.grid(row=2, column=1, padx=3, pady=3)
        #
        canvasSNRlcA = FigureCanvasTkAgg(figSNR_A, master=frameStatistical_A)
        canvasSNRlcB = FigureCanvasTkAgg(figSNR_B, master=frameStatistical_B)
        #
        canvas_widgetSNR_A = canvasSNRlcA.get_tk_widget()
        canvas_widgetSNR_A.grid(row=0, column=0, columnspan=2)

        canvas_widgetSNR_B = canvasSNRlcB.get_tk_widget()
        canvas_widgetSNR_B.grid(row=0, column=0, columnspan=2)
        # Begin the descriptive statistics to the initial raw data apply the different techniques light curve A
        lcA_snr = snr_mag_A
        HurstA, c, data = compute_Hc(lcA_snr, kind='random_walk', simplified=True)
        skewnessA = skew(lcA_snr, axis=0, bias=True)
        curtosisA = kurtosis(lcA_snr, axis=0, fisher=False, bias=True)
        resA, resB = stats.jarque_bera(lcA_snr)
        resultA = adfuller(lcA_snr)
        adfStatisticA = resultA[0]
        adfPvalueA = resultA[1]
        # Extract and print the critical values in a dictionary
        critical_values_dict = {key: value for key, value in resultA[4].items()}
        first_critical_valueA = critical_values_dict['1%']
        second_critical_valueA = critical_values_dict['5%']
        third_critical_valueA = critical_values_dict['10%']
        empty = ""
        statsA = {
            'count': lcA_snr.count(),
            'mean': lcA_snr.mean(),
            'std.dev': lcA_snr.std(),
            'min': lcA_snr.min(),
            'max': lcA_snr.max(),
            'Hurst': HurstA,
            'Skewness': skewnessA,
            'Kurtosis': curtosisA,
            'Jarque-Bera': resA,
            'P-value': resB,
            'ADF-Statistic': adfStatisticA,
            'p-value': adfPvalueA,
            'Critical-Vals': empty,
            '1%:': first_critical_valueA,
            '5%:': second_critical_valueA,
            '10%:': third_critical_valueA
        }
        # Begin the descriptive statistics to the initial raw data apply the different techniques light curve B
        lcB_snr = snr_mag_B
        HurstB, c, data = compute_Hc(lcB_snr, kind='random_walk', simplified=True)
        skewnessB = skew(lcB_snr, axis=0, bias=True)
        curtosisB = kurtosis(lcB_snr, axis=0, fisher=False, bias=True)
        resC, resD = stats.jarque_bera(lcB_snr)
        resultB = adfuller(lcB_snr)
        adfStatisticB = resultB[0]
        adfPvalueB = resultB[1]
        # Extract and print the critical values in a dictionary
        critical_values_dict = {key: value for key, value in resultA[4].items()}
        first_critical_valueB = critical_values_dict['1%']
        second_critical_valueB = critical_values_dict['5%']
        third_critical_valueB = critical_values_dict['10%']
        statsB = {
            'count': lcB_snr.count(),
            'mean': lcB_snr.mean(),
            'std.dev': lcB_snr.std(),
            'min': lcB_snr.min(),
            'max': lcB_snr.max(),
            'Hurst': HurstB,
            'Skewness': skewnessB,
            'Kurtosis': curtosisB,
            'Jarque-Bera': resC,
            'P-value': resD,
            'ADF-Statistic': adfStatisticB,
            'p-value': adfPvalueB,
            'Critical-Vals': empty,
            '1%:': first_critical_valueB,
            '5%:': second_critical_valueB,
            '10%:': third_critical_valueB
        }
        # the descriptive statistic widget
        statisticalAnalysisA = tk.Text(frameStatistical_A, width=26, height=17, bg="#00CDCD",
                                       font=("Courier", 10))  # cyan3	#00CDCD	RGB(0,205,205)
        statisticalAnalysisA.grid(row=0, column=3, columnspan=1, padx=2, pady=2)

        statisticalAnalysisB = tk.Text(frameStatistical_B, width=26, height=17, bg="#7EC0EE",
                                       font=("Courier", 10))  # skyblue2 #7EC0EE RGB(126,192,238)
        statisticalAnalysisB.grid(row=0, column=3, columnspan=1, padx=2, pady=2)
        # Create a DataFrame with a single-row index for light curve A
        df_statsA = pd.DataFrame(statsA, index=['Statistics'])
        # Transpose the DataFrame
        df_statsA_transposed = df_statsA.transpose()
        # Convert the data in the second column to numeric and apply formatting-for only two decimal points
        column_name = 'Statistics'
        df_statsA_transposed[column_name] = pd.to_numeric(df_statsA_transposed[column_name], errors='coerce').apply(
            lambda x: f'{x:.2f}' if not pd.isnull(x) else '')
        # Get the formatted DataFrame as a string without the header and index
        statsA_str = df_statsA_transposed.to_string(header=False, index=False)
        # Create a list of lines with both column names and values
        lines = [f'{col:<18}{val}' if val else f'{col}' for col, val in
                 zip(df_statsA_transposed.index, statsA_str.split('\n'))]
        # Insert lines into the Text widget with line breaks
        formatted_output_SNRlead = '\n'.join(lines)
        statisticalAnalysisA.insert(tk.END, formatted_output_SNRlead)
        # Create a DataFrame with a single-row index for light curve B
        df_statsB = pd.DataFrame(statsB, index=['Statistics'])
        # Transpose the DataFrame
        df_statsB_transposed = df_statsB.transpose()
        # Convert the data in the second column to numeric and apply formatting-for only two decimal points
        column_nameB = 'Statistics'
        df_statsB_transposed[column_nameB] = pd.to_numeric(df_statsB_transposed[column_nameB], errors='coerce').apply(
            lambda x: f'{x:.2f}' if not pd.isnull(x) else '')
        # Get the formatted DataFrame as a string without the header and index
        statsB_str = df_statsB_transposed.to_string(header=False, index=False)
        # Create a list of lines with both column names and values
        linesB = [f'{col:<18}{val}' if val else f'{col}' for col, val in
                  zip(df_statsB_transposed.index, statsB_str.split('\n'))]
        # Insert lines into the Text widget with line breaks
        formatted_output_SNRdelay = '\n'.join(linesB)
        statisticalAnalysisB.insert(tk.END, formatted_output_SNRdelay)
        ########################################################################
        # Adjust the figsize to decrease or increase the size of the graphic
        figSNR = plt.Figure(figsize=(4.7, 2.65))
        axSNR = figSNR.add_subplot(111)
        # ax.set_position is [left, bottom, width, height] by increasing the third an fourth parameter
        # the plot looks tighter
        axSNR.set_position([0.12, 0.1585, 0.85, 0.83])
        # Plot the first DataFrame
        axSNR.errorbar(lightCurve_A_SNR['time_snr'], lightCurve_A_SNR['snr_mag_A'], #HERE IS THE ERROR
                       yerr=lightCurve_A_SNR['error_A_SNR'], fmt='s', elinewidth=0.5, markersize=1,
                       label="Lead light curve")
        # Plot the second DataFrame
        axSNR.errorbar(lightCurve_B_SNR['time_snr'], lightCurve_B_SNR['snr_mag_B'],
                       yerr=lightCurve_B_SNR['error_B_SNR'], fmt='s', elinewidth=0.5, markersize=1,
                       label="Delayed light curve")
        axSNR.set_xlabel("Time (days)", fontsize=8)
        axSNR.set_ylabel("Magnitude", fontsize=8)
        axSNR.tick_params(axis="x", labelsize=6)
        axSNR.tick_params(axis="y", labelsize=6)
        axSNR.legend()
        time_snr = time_snr.tail(-1)
        snr_mag_A = pd.Series(snr_mag_A).tail(-1)
        error_A_SNR = pd.Series(error_A_SNR).tail(-1)
        snr_mag_B = pd.Series(snr_mag_B).tail(-1)
        error_B_SNR = pd.Series(error_B_SNR).tail(-1)
        ###########################################
        initial_canvas = FigureCanvasTkAgg(figSNR, master=framePlot_lcAB)
        canvas_widgetSNR = initial_canvas.get_tk_widget()
        canvas_widgetSNR.grid(row=0, column=0, columnspan=1)
        plt.show()
        colour1 = '#020f12'
        colour2 = '#DCDCDC'
        colour3 = '#C1CDC1'
        colour4 = '#292421'
        export_button = tk.Button(root, background=colour2, foreground=colour4, activebackground=colour3,
                           activeforeground=colour4, highlightthickness=4, highlightbackground=colour2,
                           highlightcolor='BLUE', width=28, height=1, border=2, cursor='hand1', font=('Arial', 13, 'bold'), text="Export descriptive statistics to PDF",
                           command = lambda: export_histogram_and_stats_to_pdf(
                    figures=[figSNR_A, figSNR_B],
                    stats_data=[formatted_output_SNRlead, formatted_output_SNRdelay],
                    headers=['Descriptive Statistics for Lead Light Curve with SNR', 'Descriptive Statistics for Delayed Light Curve with SNR'],
                    additional_figure=figSNR,
                    additional_header="Light Curves in Simple Net Return",
                    initial_dir =os.path.expanduser('~'),
                    initial_file ="Plot_and_Statistics_with_SNR.pdf"
                    ))
        export_button.grid(row=0, column=1, pady=10)
        #################
    elif preprocessing_selectionSA == 'Wavelet Denoise lvl 1':
        # Remove the frame and canvas from the grid layout
        if frameStatistical_A:
            frameStatistical_A.grid_forget()
        if frameStatistical_B:
            frameStatistical_B.grid_forget()
        df_A = series_data[1].copy()
        df_B = series_data[2].copy()
        # Calculate the pct error of each curve
        dfA = series_data[1].copy()
        dfB = series_data[2].copy()
        # Series to get the size or quantity of observations in the light curves, in order to plot in contiunous form
        untilData = len(dfA['time'])
        mylist = list(range(untilData))
        timeRaw = mylist
        # calculate the percentage error
        pct_err_A = dfA['error'] / dfA['Magnitude']
        pct_err_B = dfB['error'] / dfB['Magnitude']
        # Resize and standarized the light curves for visual purposes
        scalerA = MinMaxScaler(feature_range=(0.15, 0.25))
        scalerB = MinMaxScaler(feature_range=(0.1, 0.2))

        dfA['Magnitude'] = scalerA.fit_transform(dfA['Magnitude'].values.reshape(-1, 1)).flatten()
        dfB['Magnitude'] = scalerB.fit_transform(dfB['Magnitude'].values.reshape(-1, 1)).flatten()
        # recalculate the error with standarized data
        err_A = abs(dfA['Magnitude'] * pct_err_A)
        err_B = abs(dfB['Magnitude'] * pct_err_B)
        lightCurve_A_raw = {
            'time': timeRaw,
            'lc_A': dfA['Magnitude'],
            'err_A': err_A,
        }
        lightCurve_B_raw = {
            'time': timeRaw,
            'lc_B': dfB['Magnitude'],
            'err_B': err_B,
        }
        time = mylist
        x = dfA['time'].to_numpy()
        x = np.reshape(x, (len(x), 1))  # ensure the index is in only one dimension
        dfA.rename(columns={"Julian_day": "time", "Magnitude": "lc_A", "error": "error_A"}, inplace=True)
        dfA['pctErr_A'] = dfA['error_A'] / dfA['lc_A']
        dfB.rename(columns={"Julian_day": "time", "Magnitude": "lc_B", "error": "error_B"}, inplace=True)
        dfB['pctErr_B'] = dfB['error_B'] / dfB['lc_B']
        # Apply the Wavelet denoise algorithm to both light curves
        y_denoise = denoise_wavelet(dfA['lc_A'], method='VisuShrink', mode='soft', wavelet_levels=1, wavelet='coif17',
                                    rescale_sigma='True')
        y1_denoise = denoise_wavelet(dfB['lc_B'], method='VisuShrink', mode='soft', wavelet_levels=1, wavelet='coif17',
                                     rescale_sigma='True')
        # Converting the denoised numpy array (light curve A) to a dataframe column and compute the error
        dfWavDenoise_lcA = pd.DataFrame(y_denoise)
        dfWavDenoise_lcB = pd.DataFrame(y1_denoise)
        dfWavDenoise_lcA = scalerA.fit_transform(dfWavDenoise_lcA.values.reshape(-1, 1)).flatten()
        dfWavDenoise_lcB = scalerB.fit_transform(dfWavDenoise_lcB.values.reshape(-1, 1)).flatten()
        # Converting the denoised numpy array (light curve A and B) to a dataframe column and calculating the error
        lcA_WavErr = abs(dfWavDenoise_lcA * dfA['pctErr_A'])
        lcB_WavErr = abs(dfWavDenoise_lcB * dfB['pctErr_B'])
        # The descriptive statistic denoised light curve A and B, we get another copy of the light curves for analysis
        df_A.rename(columns={"Julian_day": "time", "Magnitude": "lc_A", "error": "error_A"}, inplace=True)
        df_B.rename(columns={"Julian_day": "time", "Magnitude": "lc_B", "error": "error_B"}, inplace=True)
        denoiseA = denoise_wavelet(df_A['lc_A'], method='VisuShrink', mode='soft', wavelet_levels=1, wavelet='coif17',
                                   rescale_sigma='True')
        denoiseB = denoise_wavelet(df_B['lc_B'], method='VisuShrink', mode='soft', wavelet_levels=1, wavelet='coif17',
                                   rescale_sigma='True')
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
        # Adjust the figsize to decrease or increase the size of the graphic
        figWD1lc = plt.Figure(figsize=(4.7, 2.65))
        axWD1 = figWD1lc.add_subplot(111)
        # ax.set_position is [left, bottom, width, height] by increasing the third an fourth parameter-the plot looks tighter
        axWD1.set_position([0.1285, 0.1585, 0.85, 0.83])
        # Plot the first DataFrame
        axWD1.errorbar(lightCurve_A_raw['time'], lightCurve_A_raw['lc_A'], yerr=lightCurve_A_raw['err_A'], fmt='s',
                       elinewidth=0.1, linewidth=0.1, markersize=2, color='red', label="Lead raw light curve")
        axWD1.plot(lightCurve_A_raw['time'], lightCurve_A_raw['lc_A'], linestyle='-', linewidth=2.5, color='red')
        # Plot the second DataFrame
        axWD1.errorbar(lightCurve_B_raw['time'], lightCurve_B_raw['lc_B'], yerr=lightCurve_B_raw['err_B'], fmt='s',
                       elinewidth=0.1, linewidth=0.1, markersize=2, color='blue', label="Delayed raw light curve")
        axWD1.plot(lightCurve_B_raw['time'], lightCurve_B_raw['lc_B'], linestyle='-', linewidth=2.5, color='blue')

        axWD1.errorbar(lightCurve_A['time'], lightCurve_A['dfWavDenoise_lcA'], yerr=lightCurve_A['lcA_WavErr'], fmt='s',
                       elinewidth=0.1, linewidth=0.1, markersize=2, color='black', label="Lead light curve with WD1")
        axWD1.plot(lightCurve_A['time'], lightCurve_A['dfWavDenoise_lcA'], linestyle='-', linewidth=1.3, color='black')
        # Plot the second DataFrame
        axWD1.errorbar(lightCurve_B['time'], lightCurve_B['dfWavDenoise_lcB'], yerr=lightCurve_B['lcB_WavErr'], fmt='s',
                       elinewidth=0.1, linewidth=0.1, markersize=2, color='magenta', label="Delayed light curve with WD1")
        axWD1.plot(lightCurve_B['time'], lightCurve_B['dfWavDenoise_lcB'], linestyle='-', linewidth=1.3,
                   color='magenta')
        axWD1.set_xlabel("Time (days) continous form", fontsize=8)
        axWD1.set_ylabel("Lead lc offset 0.15, Delayed lc offset 0.1, raw & denoised\nMagnitude", fontsize=6)
        # Change the font size for the specific label
        axWD1.tick_params(axis="x", labelsize=6)
        axWD1.tick_params(axis="y", labelsize=6)
        axWD1.legend(fontsize="7")
        ###########################################
        initial_canvas = FigureCanvasTkAgg(figWD1lc, master=framePlot_lcAB)
        canvas_widgetWD1 = initial_canvas.get_tk_widget()
        canvas_widgetWD1.grid(row=0, column=0, columnspan=1)
        # Adjust the Canvas widget's size to make the figure smaller
        figWD1_A = plt.Figure(figsize=(2.5, 1.95))
        lcA_WD1_hst = figWD1_A.add_subplot(111)
        lcA_WD1_hst.hist(y_denoise, bins=10, alpha=0.5, color="blue", ec="black", lw=3)
        lcA_WD1_hst.set_title("Lead light curve with WD1", fontsize=8)  # Add title to histogram A
        lcA_WD1_hst.tick_params(axis="x", labelsize=6)
        lcA_WD1_hst.tick_params(axis="y", labelsize=6)

        figWD1_B = plt.Figure(figsize=(2.5, 1.95))
        lcB_WD1_hst = figWD1_B.add_subplot(111)
        lcB_WD1_hst.hist(y1_denoise, bins=10, alpha=0.5, color="#8B7B8B", ec="black", lw=3)  # 8B7B8B
        lcB_WD1_hst.set_title("Delayed light curve with WD1", fontsize=8)  # Add title to histogram A
        lcB_WD1_hst.tick_params(axis="x", labelsize=6)
        lcB_WD1_hst.tick_params(axis="y", labelsize=6)
        # Create a Frame to hold the widgets
        frameStatistical_A = tk.Frame(root)
        frameStatistical_B = tk.Frame(root)
        frameStatistical_A.grid(row=1, column=1, padx=3, pady=3)
        frameStatistical_B.grid(row=2, column=1, padx=3, pady=3)
        #
        canvasWD1lcA = FigureCanvasTkAgg(figWD1_A, master=frameStatistical_A)
        canvasWD1lcB = FigureCanvasTkAgg(figWD1_B, master=frameStatistical_B)
        #
        canvas_widgetWD1_A = canvasWD1lcA.get_tk_widget()
        canvas_widgetWD1_A.grid(row=0, column=0, columnspan=2)

        canvas_widgetWD1_B = canvasWD1lcB.get_tk_widget()
        canvas_widgetWD1_B.grid(row=0, column=0, columnspan=2)
        # Begin the descriptive statistics to the initial raw data apply the different techniques light curve A
        lcA_WD1 = pd.DataFrame(denoiseA)
        HurstA, c, data = compute_Hc(lcA_WD1, kind='random_walk', simplified=True)
        skewnessA = skew(lcA_WD1, axis=0, bias=True)
        curtosisA = kurtosis(lcA_WD1, axis=0, fisher=False, bias=True)
        resA, resB = stats.jarque_bera(lcA_WD1)
        resultA = adfuller(lcA_WD1)
        adfStatisticA = resultA[0]
        adfPvalueA = resultA[1]
        # Extract and print the critical values in a dictionary
        critical_values_dict = {key: value for key, value in resultA[4].items()}
        first_critical_valueA = critical_values_dict['1%']
        second_critical_valueA = critical_values_dict['5%']
        third_critical_valueA = critical_values_dict['10%']
        empty = ""
        statsA = {
            'count': lcA_WD1.count().values[0],
            'mean': lcA_WD1.mean().values[0],
            'std.dev': lcA_WD1.std().values[0],
            'min': lcA_WD1.min().values[0],
            'max': lcA_WD1.max().values[0],
            'Hurst': HurstA,
            'Skewness': skewnessA,
            'Kurtosis': curtosisA,
            'Jarque-Bera': resA,
            'P-value': resB,
            'ADF-Statistic': adfStatisticA,
            'p-value': adfPvalueA,
            'Critical-Vals': empty,
            '1%:': first_critical_valueA,
            '5%:': second_critical_valueA,
            '10%:': third_critical_valueA
        }
        # Begin the descriptive statistics to the initial raw data apply the different techniques light curve B
        lcB_WD1 = pd.DataFrame(denoiseB)
        HurstB, c, data = compute_Hc(lcB_WD1, kind='random_walk', simplified=True)
        skewnessB = skew(lcB_WD1, axis=0, bias=True)
        curtosisB = kurtosis(lcB_WD1, axis=0, fisher=False, bias=True)
        resC, resD = stats.jarque_bera(lcB_WD1)
        resultB = adfuller(lcB_WD1)
        adfStatisticB = resultB[0]
        adfPvalueB = resultB[1]
        # Extract and print the critical values in a dictionary
        critical_values_dict = {key: value for key, value in resultA[4].items()}
        first_critical_valueB = critical_values_dict['1%']
        second_critical_valueB = critical_values_dict['5%']
        third_critical_valueB = critical_values_dict['10%']
        statsB = {
            'count': lcB_WD1.count().values[0],
            'mean': lcB_WD1.mean().values[0],
            'std.dev': lcB_WD1.std().values[0],
            'min': lcB_WD1.min().values[0],
            'max': lcB_WD1.max().values[0],
            'Hurst': HurstB,
            'Skewness': skewnessB,
            'Kurtosis': curtosisB,
            'Jarque-Bera': resC,
            'P-value': resD,
            'ADF-Statistic': adfStatisticB,
            'p-value': adfPvalueB,
            'Critical-Vals': empty,
            '1%:': first_critical_valueB,
            '5%:': second_critical_valueB,
            '10%:': third_critical_valueB
        }
        # the descriptive statistic widget
        statisticalAnalysisA = tk.Text(frameStatistical_A, width=26, height=17, bg="#00CDCD",
                                       font=("Courier", 10))  # cyan3	#00CDCD	RGB(0,205,205)
        statisticalAnalysisA.grid(row=0, column=3, columnspan=1, padx=2, pady=2)

        statisticalAnalysisB = tk.Text(frameStatistical_B, width=26, height=17, bg="#7EC0EE",
                                       font=("Courier", 10))  # skyblue2 #7EC0EE RGB(126,192,238)
        statisticalAnalysisB.grid(row=0, column=3, columnspan=1, padx=2, pady=2)
        # Create a DataFrame with a single-row index for light curve A
        df_statsA = pd.DataFrame(statsA, index=['Statistics'])
        # Transpose the DataFrame
        df_statsA_transposed = df_statsA.transpose()
        # Convert the data in the second column to numeric and apply formatting-for only two decimal points
        column_name = 'Statistics'
        df_statsA_transposed[column_name] = pd.to_numeric(df_statsA_transposed[column_name], errors='coerce').apply(
            lambda x: f'{x:.2f}' if not pd.isnull(x) else '')
        # Get the formatted DataFrame as a string without the header and index
        statsA_str = df_statsA_transposed.to_string(header=False, index=False)
        # Create a list of lines with both column names and values
        lines = [f'{col:<18}{val}' if val else f'{col}' for col, val in
                 zip(df_statsA_transposed.index, statsA_str.split('\n'))]
        # Insert lines into the Text widget with line breaks
        formatted_output_WD1_lead = '\n'.join(lines)
        statisticalAnalysisA.insert(tk.END, formatted_output_WD1_lead)
        # Create a DataFrame with a single-row index for light curve B
        df_statsB = pd.DataFrame(statsB, index=['Statistics'])
        # Transpose the DataFrame
        df_statsB_transposed = df_statsB.transpose()
        # Convert the data in the second column to numeric and apply formatting-for only two decimal points
        column_nameB = 'Statistics'
        df_statsB_transposed[column_nameB] = pd.to_numeric(df_statsB_transposed[column_nameB], errors='coerce').apply(
            lambda x: f'{x:.2f}' if not pd.isnull(x) else '')
        # Get the formatted DataFrame as a string without the header and index
        statsB_str = df_statsB_transposed.to_string(header=False, index=False)
        # Create a list of lines with both column names and values
        linesB = [f'{col:<18}{val}' if val else f'{col}' for col, val in
                  zip(df_statsB_transposed.index, statsB_str.split('\n'))]
        # Insert lines into the Text widget with line breaks
        formatted_output_WD1_delay = '\n'.join(linesB)
        statisticalAnalysisB.insert(tk.END, formatted_output_WD1_delay)
        plt.show()
        colour1 = '#020f12'
        colour2 = '#DCDCDC'
        colour3 = '#C1CDC1'
        colour4 = '#292421'
        export_button = tk.Button(root, background=colour2, foreground=colour4, activebackground=colour3,
                           activeforeground=colour4, highlightthickness=4, highlightbackground=colour2,
                           highlightcolor='BLUE', width=28, height=1, border=2, cursor='hand1', font=('Arial', 13, 'bold'), text="Export descriptive statistics to PDF",
                                command =  lambda: export_histogram_and_stats_to_pdf(
                                figures=[figWD1_A, figWD1_B],
                                stats_data=[formatted_output_WD1_lead, formatted_output_WD1_delay],
                                headers=['Descriptive Statistics for Lead Light Curve with WD1', 'Descriptive Statistics for Delayed Light Curve with WD1'],
                                additional_figure=figWD1lc,
                                additional_header="Light Curves with Raw Data and Wavelet Denoise lvl 1",
                                initial_dir=os.path.expanduser('~'),
                                initial_file="Plot_and_Statistics_WD_level1.pdf"
                                ))
        export_button.grid(row=0, column=1, pady=10)
    elif preprocessing_selectionSA == 'Wavelet Denoise lvl 2':
        # Remove the frame and canvas from the grid layout
        if frameStatistical_A:
            frameStatistical_A.grid_forget()
        if frameStatistical_B:
            frameStatistical_B.grid_forget()
            # Calculate the pct error of each curve
        df_A = series_data[1].copy()  # copy for statistical analysis
        df_B = series_data[2].copy()  # copy for statistical analysis
        dfA = series_data[1].copy()
        dfB = series_data[2].copy()
        # Create the data for the raw data and the first step is to put the time in a continous form
        untilData = len(dfA['time'])
        mylist = list(range(untilData))
        timeRaw = mylist
        # Calculate the percentage error
        pct_err_A = dfA['error'] / dfA['Magnitude']
        pct_err_B = dfB['error'] / dfB['Magnitude']
        # Standarized the light curves for visual purposes in plot
        scalerA = MinMaxScaler(feature_range=(0.15, 0.25))
        scalerB = MinMaxScaler(feature_range=(0.1, 0.2))

        dfA['Magnitude'] = scalerA.fit_transform(dfA['Magnitude'].values.reshape(-1, 1)).flatten()
        dfB['Magnitude'] = scalerB.fit_transform(dfB['Magnitude'].values.reshape(-1, 1)).flatten()
        # recalculate the error with standarized data
        err_A = abs(dfA['Magnitude'] * pct_err_A)
        err_B = abs(dfB['Magnitude'] * pct_err_B)

        lightCurve_A_raw = {
            'time': timeRaw,
            'lc_A': dfA['Magnitude'],
            'err_A': err_A,
        }
        lightCurve_B_raw = {
            'time': timeRaw,
            'lc_B': dfB['Magnitude'],
            'err_B': err_B,
        }
        time = mylist
        x = dfA['time'].to_numpy()
        x = np.reshape(x, (len(x), 1))  # ensure the index is in only one dimension

        dfA.rename(columns={"Julian_day": "time", "Magnitude": "lc_A", "error": "error_A"}, inplace=True)
        dfA['pctErr_A'] = dfA['error_A'] / dfA['lc_A']
        dfB.rename(columns={"Julian_day": "time", "Magnitude": "lc_B", "error": "error_B"}, inplace=True)
        dfB['pctErr_B'] = dfB['error_B'] / dfB['lc_B']
        # Apply the Wavelet denoise algorithm to both light curves
        y_denoise = denoise_wavelet(dfA['lc_A'], method='VisuShrink', mode='soft', wavelet_levels=2, wavelet='coif17',
                                    rescale_sigma='True')
        y1_denoise = denoise_wavelet(dfB['lc_B'], method='VisuShrink', mode='soft', wavelet_levels=2, wavelet='coif17',
                                     rescale_sigma='True')
        # Converting the denoised numpy array (light curve A) to a dataframe column and ocalculating the error
        dfWavDenoise_lcA = pd.DataFrame(y_denoise)
        dfWavDenoise_lcB = pd.DataFrame(y1_denoise)
        # Scaling or standarizing the denoised data
        dfWavDenoise_lcA = scalerA.fit_transform(dfWavDenoise_lcA.values.reshape(-1, 1)).flatten()
        dfWavDenoise_lcB = scalerB.fit_transform(dfWavDenoise_lcB.values.reshape(-1, 1)).flatten()
        # Converting the denoised numpy array (light curve A and B) to a dataframe column and calculating the error
        lcA_WavErr = abs(dfWavDenoise_lcA * dfA['pctErr_A'])
        lcB_WavErr = abs(dfWavDenoise_lcB * dfB['pctErr_B'])
        # The descriptive statistic denoised light curve A and B, we get another copy of the light curves for analysis
        df_A.rename(columns={"Julian_day": "time", "Magnitude": "lc_A", "error": "error_A"}, inplace=True)
        df_B.rename(columns={"Julian_day": "time", "Magnitude": "lc_B", "error": "error_B"}, inplace=True)
        denoiseA_WD2 = denoise_wavelet(df_A['lc_A'], method='VisuShrink', mode='soft', wavelet_levels=2,
                                       wavelet='coif17', rescale_sigma='True')
        denoiseB_WD2 = denoise_wavelet(df_B['lc_B'], method='VisuShrink', mode='soft', wavelet_levels=2,
                                       wavelet='coif17', rescale_sigma='True')
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
        # Adjust the figsize to decrease or increase the size of the graphic
        figWD2lc = plt.Figure(figsize=(4.7, 2.65))
        axWD1 = figWD2lc.add_subplot(111)
        # ax.set_position is [left, bottom, width, height] by increasing the third an fourth parameter-the plot looks tighter
        axWD1.set_position([0.1285, 0.1585, 0.85, 0.83])
        # Plot the first DataFrame
        axWD1.errorbar(lightCurve_A_raw['time'], lightCurve_A_raw['lc_A'], yerr=lightCurve_A_raw['err_A'], fmt='s',
                       elinewidth=0.1, linewidth=0.1, markersize=2, color='red', label="Lead raw light curve")
        axWD1.plot(lightCurve_A_raw['time'], lightCurve_A_raw['lc_A'], linestyle='-', linewidth=2.5, color='red')
        # Plot the second DataFrame
        axWD1.errorbar(lightCurve_B_raw['time'], lightCurve_B_raw['lc_B'], yerr=lightCurve_B_raw['err_B'], fmt='s',
                       elinewidth=0.1, linewidth=0.1, markersize=2, color='blue', label="Delayed raw light curve")
        axWD1.plot(lightCurve_B_raw['time'], lightCurve_B_raw['lc_B'], linestyle='-', linewidth=2.5, color='blue')

        axWD1.errorbar(lightCurve_A['time'], lightCurve_A['dfWavDenoise_lcA'], yerr=lightCurve_A['lcA_WavErr'], fmt='s',
                       elinewidth=0.1, linewidth=0.1, markersize=2, color='black', label="Lead light curve with WD2")
        axWD1.plot(lightCurve_A['time'], lightCurve_A['dfWavDenoise_lcA'], linestyle='-', linewidth=1.3, color='black')
        # Plot the second DataFrame
        axWD1.errorbar(lightCurve_B['time'], lightCurve_B['dfWavDenoise_lcB'], yerr=lightCurve_B['lcB_WavErr'], fmt='s',
                       elinewidth=0.1, linewidth=0.1, markersize=2, color='magenta', label="Delayed light curve with WD2")
        axWD1.plot(lightCurve_B['time'], lightCurve_B['dfWavDenoise_lcB'], linestyle='-', linewidth=1.3,
                   color='magenta')
        axWD1.set_xlabel("Time (days) continous form", fontsize=8)
        axWD1.set_ylabel("Lead lc offset 0.15, delayed lc offset 0.1, raw & denoised\nMagnitude", fontsize=6)
        # Change the font size for the specific label
        axWD1.tick_params(axis="x", labelsize=6)
        axWD1.tick_params(axis="y", labelsize=6)
        axWD1.legend(fontsize="7")
        ###########################################
        initial_canvas = FigureCanvasTkAgg(figWD2lc, master=framePlot_lcAB)
        canvas_widgetWD1 = initial_canvas.get_tk_widget()
        canvas_widgetWD1.grid(row=0, column=0, columnspan=1)
        # Adjust the Canvas widget's size to make the figure smaller or bigger
        figWD2_A = plt.Figure(figsize=(2.5, 1.95))
        lcA_WD1_hst = figWD2_A.add_subplot(111)

        lcA_WD1_hst.hist(y_denoise, bins=10, alpha=0.5, color="blue", ec="black", lw=3)
        lcA_WD1_hst.set_title("Lead light curve with WD2", fontsize=8)  # Add title to histogram A
        lcA_WD1_hst.tick_params(axis="x", labelsize=6)
        lcA_WD1_hst.tick_params(axis="y", labelsize=6)
        figWD2_B = plt.Figure(figsize=(2.5, 1.95))
        lcB_WD1_hst = figWD2_B.add_subplot(111)

        lcB_WD1_hst.hist(y1_denoise, bins=10, alpha=0.5, color="#8B7B8B", ec="black", lw=3)  # 8B7B8B
        lcB_WD1_hst.set_title("Delayed light curve with WD2", fontsize=8)  # Add title to histogram A
        lcB_WD1_hst.tick_params(axis="x", labelsize=6)
        lcB_WD1_hst.tick_params(axis="y", labelsize=6)
        # Create a Frame to hold the widgets
        frameStatistical_A = tk.Frame(root)
        frameStatistical_B = tk.Frame(root)
        frameStatistical_A.grid(row=1, column=1, padx=3, pady=3)
        frameStatistical_B.grid(row=2, column=1, padx=3, pady=3)
        #
        canvasWD1lcA = FigureCanvasTkAgg(figWD2_A, master=frameStatistical_A)
        canvasWD1lcB = FigureCanvasTkAgg(figWD2_B, master=frameStatistical_B)
        #
        canvas_widgetWD1_A = canvasWD1lcA.get_tk_widget()
        canvas_widgetWD1_A.grid(row=0, column=0, columnspan=2)

        canvas_widgetWD1_B = canvasWD1lcB.get_tk_widget()
        canvas_widgetWD1_B.grid(row=0, column=0, columnspan=2)
        # Begin the descriptive statistics to the initial raw data apply the different techniques light curve A
        lcA_WD2 = pd.DataFrame(denoiseA_WD2)
        HurstA, c, data = compute_Hc(lcA_WD2, kind='random_walk', simplified=True)
        skewnessA = skew(lcA_WD2, axis=0, bias=True)
        curtosisA = kurtosis(lcA_WD2, axis=0, fisher=False, bias=True)
        resA, resB = stats.jarque_bera(lcA_WD2)
        resultA = adfuller(lcA_WD2)
        adfStatisticA = resultA[0]
        adfPvalueA = resultA[1]
        # Extract and print the critical values in a dictionary
        critical_values_dict = {key: value for key, value in resultA[4].items()}
        first_critical_valueA = critical_values_dict['1%']
        second_critical_valueA = critical_values_dict['5%']
        third_critical_valueA = critical_values_dict['10%']
        empty = ""
        statsA = {
            'count': lcA_WD2.count().values[0],
            'mean': lcA_WD2.mean().values[0],
            'std.dev': lcA_WD2.std().values[0],
            'min': lcA_WD2.min().values[0],
            'max': lcA_WD2.max().values[0],
            'Hurst': HurstA,
            'Skewness': skewnessA,
            'Kurtosis': curtosisA,
            'Jarque-Bera': resA,
            'P-value': resB,
            'ADF-Statistic': adfStatisticA,
            'p-value': adfPvalueA,
            'Critical-Vals': empty,
            '1%:': first_critical_valueA,
            '5%:': second_critical_valueA,
            '10%:': third_critical_valueA
        }
        # Begin the descriptive statistics to the initial raw data apply the different techniques light curve B
        lcB_WD2 = pd.DataFrame(denoiseB_WD2)
        HurstB, c, data = compute_Hc(lcB_WD2, kind='random_walk', simplified=True)
        skewnessB = skew(lcB_WD2, axis=0, bias=True)
        curtosisB = kurtosis(lcB_WD2, axis=0, fisher=False, bias=True)
        resC, resD = stats.jarque_bera(lcB_WD2)
        resultB = adfuller(lcB_WD2)
        adfStatisticB = resultB[0]
        adfPvalueB = resultB[1]
        # Extract and print the critical values in a dictionary
        critical_values_dict = {key: value for key, value in resultA[4].items()}
        first_critical_valueB = critical_values_dict['1%']
        second_critical_valueB = critical_values_dict['5%']
        third_critical_valueB = critical_values_dict['10%']
        statsB = {
            'count': lcB_WD2.count().values[0],
            'mean': lcB_WD2.mean().values[0],
            'std.dev': lcB_WD2.std().values[0],
            'min': lcB_WD2.min().values[0],
            'max': lcB_WD2.max().values[0],
            'Hurst': HurstB,
            'Skewness': skewnessB,
            'Kurtosis': curtosisB,
            'Jarque-Bera': resC,
            'P-value': resD,
            'ADF-Statistic': adfStatisticB,
            'p-value': adfPvalueB,
            'Critical-Vals': empty,
            '1%:': first_critical_valueB,
            '5%:': second_critical_valueB,
            '10%:': third_critical_valueB
        }
        # the descriptive statistic widget
        statisticalAnalysisA = tk.Text(frameStatistical_A, width=26, height=17, bg="#00CDCD",
                                       font=("Courier", 10))  # cyan3	#00CDCD	RGB(0,205,205)
        statisticalAnalysisA.grid(row=0, column=3, columnspan=1, padx=2, pady=2)
        statisticalAnalysisB = tk.Text(frameStatistical_B, width=26, height=17, bg="#7EC0EE",
                                       font=("Courier", 10))  # skyblue2 #7EC0EE RGB(126,192,238)
        statisticalAnalysisB.grid(row=0, column=3, columnspan=1, padx=2, pady=2)
        # Create a DataFrame with a single-row index for light curve A
        df_statsA = pd.DataFrame(statsA, index=['Statistics'])
        # Transpose the DataFrame
        df_statsA_transposed = df_statsA.transpose()
        # Convert the data in the second column to numeric and apply formatting-for only two decimal points
        column_name = 'Statistics'
        df_statsA_transposed[column_name] = pd.to_numeric(df_statsA_transposed[column_name], errors='coerce').apply(
            lambda x: f'{x:.2f}' if not pd.isnull(x) else '')
        # Get the formatted DataFrame as a string without the header and index
        statsA_str = df_statsA_transposed.to_string(header=False, index=False)
        # Create a list of lines with both column names and values
        lines = [f'{col:<18}{val}' if val else f'{col}' for col, val in
                 zip(df_statsA_transposed.index, statsA_str.split('\n'))]
        # Insert lines into the Text widget with line breaks
        formatted_output_WD2_lead = '\n'.join(lines)
        statisticalAnalysisA.insert(tk.END, formatted_output_WD2_lead)
        # Create a DataFrame with a single-row index for light curve B
        df_statsB = pd.DataFrame(statsB, index=['Statistics'])
        # Transpose the DataFrame
        df_statsB_transposed = df_statsB.transpose()
        # Convert the data in the second column to numeric and apply formatting-for only two decimal points
        column_nameB = 'Statistics'
        df_statsB_transposed[column_nameB] = pd.to_numeric(df_statsB_transposed[column_nameB], errors='coerce').apply(
            lambda x: f'{x:.2f}' if not pd.isnull(x) else '')
        # Get the formatted DataFrame as a string without the header and index
        statsB_str = df_statsB_transposed.to_string(header=False, index=False)
        # Create a list of lines with both column names and values
        linesB = [f'{col:<18}{val}' if val else f'{col}' for col, val in
                  zip(df_statsB_transposed.index, statsB_str.split('\n'))]
        # Insert lines into the Text widget with line breaks
        formatted_output_WD2_delay = '\n'.join(linesB)
        statisticalAnalysisB.insert(tk.END, formatted_output_WD2_delay)
        plt.show()
        colour1 = '#020f12'
        colour2 = '#DCDCDC'
        colour3 = '#C1CDC1'
        colour4 = '#292421'
        export_button = tk.Button(root, background=colour2, foreground=colour4, activebackground=colour3,
                          activeforeground=colour4, highlightthickness=4, highlightbackground=colour2,
                          highlightcolor='BLUE', width=28, height=1, border=2, cursor='hand1',
                          font=('Arial', 13, 'bold'),
                          text="Export descriptive statistics to PDF",
                                command =  lambda: export_histogram_and_stats_to_pdf(
                                figures=[figWD2_A, figWD2_B],
                                stats_data=[formatted_output_WD2_lead, formatted_output_WD2_delay],
                                headers=['Descriptive Statistics for Lead Light Curve with WD2', 'Descriptive Statistics for Delayed Light Curve with WD2'],
                                additional_figure=figWD2lc,
                                additional_header="Light Curves with Raw Data and Wavelet Denoise lvl 2",
                                initial_dir=os.path.expanduser('~'),
                                initial_file="Plot_and_Statistics_WD_level2.pdf"
                                ))
        export_button.grid(row=0, column=1, pady=10)
    elif preprocessing_selectionSA == 'Wavelet Denoise lvl 3':
        # Remove the frame and canvas from the grid layout
        if frameStatistical_A:
            frameStatistical_A.grid_forget()
        if frameStatistical_B:
            frameStatistical_B.grid_forget()
            # Calculate the pct error of each curve
        df_A = series_data[1].copy()  # copy for statistical analysis
        df_B = series_data[2].copy()  # copy for statistical analysis
        dfA = series_data[1].copy()
        dfB = series_data[2].copy()
        # Create the data for the raw data and the first step is to put the time in a continous form
        untilData = len(dfA['time'])
        mylist = list(range(untilData))
        timeRaw = mylist
        # calculate the percentage error
        pct_err_A = dfA['error'] / dfA['Magnitude']
        pct_err_B = dfB['error'] / dfB['Magnitude']
        # Standarized the light curves for visual purposes in the plot
        scalerA = MinMaxScaler(feature_range=(0.15, 0.25))
        scalerB = MinMaxScaler(feature_range=(0.1, 0.2))
        dfA['Magnitude'] = scalerA.fit_transform(dfA['Magnitude'].values.reshape(-1, 1)).flatten()
        dfB['Magnitude'] = scalerB.fit_transform(dfB['Magnitude'].values.reshape(-1, 1)).flatten()
        # recalculate the error with standarized data
        err_A = abs(dfA['Magnitude'] * pct_err_A)
        err_B = abs(dfB['Magnitude'] * pct_err_B)
        lightCurve_A_raw = {
            'time': timeRaw,
            'lc_A': dfA['Magnitude'],
            'err_A': err_A,
        }
        lightCurve_B_raw = {
            'time': timeRaw,
            'lc_B': dfB['Magnitude'],
            'err_B': err_B,
        }
        time = mylist
        x = dfA['time'].to_numpy()
        x = np.reshape(x, (len(x), 1))  # ensure the index is in only one dimension

        dfA.rename(columns={"Julian_day": "time", "Magnitude": "lc_A", "error": "error_A"}, inplace=True)
        dfA['pctErr_A'] = dfA['error_A'] / dfA['lc_A']
        dfB.rename(columns={"Julian_day": "time", "Magnitude": "lc_B", "error": "error_B"}, inplace=True)
        dfB['pctErr_B'] = dfB['error_B'] / dfB['lc_B']
        # Apply the Wavelet denoise algorithm to both light curves
        y_denoise = denoise_wavelet(dfA['lc_A'], method='VisuShrink', mode='soft', wavelet_levels=3, wavelet='coif17',
                                    rescale_sigma='True')
        y1_denoise = denoise_wavelet(dfB['lc_B'], method='VisuShrink', mode='soft', wavelet_levels=3, wavelet='coif17',
                                     rescale_sigma='True')
        # Converting the denoised numpy array (light curve A) to a dataframe column and ocalculating the error
        dfWavDenoise_lcA = pd.DataFrame(y_denoise)
        dfWavDenoise_lcB = pd.DataFrame(y1_denoise)
        # Scaling or standarizing the denoised data
        dfWavDenoise_lcA = scalerA.fit_transform(dfWavDenoise_lcA.values.reshape(-1, 1)).flatten()
        dfWavDenoise_lcB = scalerB.fit_transform(dfWavDenoise_lcB.values.reshape(-1, 1)).flatten()
        # Converting the denoised numpy array (light curve A and B) to a dataframe column and calculating the error
        lcA_WavErr = abs(dfWavDenoise_lcA * dfA['pctErr_A'])
        lcB_WavErr = abs(dfWavDenoise_lcB * dfB['pctErr_B'])
        # The descriptive statistic denoised light curve A and B, we get another copy of the light curves for analysis
        df_A.rename(columns={"Julian_day": "time", "Magnitude": "lc_A", "error": "error_A"}, inplace=True)
        df_B.rename(columns={"Julian_day": "time", "Magnitude": "lc_B", "error": "error_B"}, inplace=True)
        denoiseA_WD3 = denoise_wavelet(df_A['lc_A'], method='VisuShrink', mode='soft', wavelet_levels=3,
                                       wavelet='coif17', rescale_sigma='True')
        denoiseB_WD3 = denoise_wavelet(df_B['lc_B'], method='VisuShrink', mode='soft', wavelet_levels=3,
                                       wavelet='coif17', rescale_sigma='True')
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
        # Adjust the figsize to decrease or increase the size of the graphic
        figWD3lc = plt.Figure(figsize=(4.7, 2.65))
        axWD1 = figWD3lc.add_subplot(111)
        # ax.set_position is [left, bottom, width, height] by increasing the third an fourth parameter-the plot looks tighter
        axWD1.set_position([0.13, 0.1585, 0.85, 0.83])
        # Plot the first DataFrame
        axWD1.errorbar(lightCurve_A_raw['time'], lightCurve_A_raw['lc_A'], yerr=lightCurve_A_raw['err_A'], fmt='s',
                       elinewidth=0.1, linewidth=0.1, markersize=2, color='red', label="Lead raw light curve")
        axWD1.plot(lightCurve_A_raw['time'], lightCurve_A_raw['lc_A'], linestyle='-', linewidth=2.5, color='red')
        # Plot the second DataFrame
        axWD1.errorbar(lightCurve_B_raw['time'], lightCurve_B_raw['lc_B'], yerr=lightCurve_B_raw['err_B'], fmt='s',
                       elinewidth=0.1, linewidth=0.1, markersize=2, color='blue', label="Delayed raw light curve")
        axWD1.plot(lightCurve_B_raw['time'], lightCurve_B_raw['lc_B'], linestyle='-', linewidth=2.5, color='blue')

        axWD1.errorbar(lightCurve_A['time'], lightCurve_A['dfWavDenoise_lcA'], yerr=lightCurve_A['lcA_WavErr'], fmt='s',
                       elinewidth=0.1, linewidth=0.1, markersize=2, color='black', label="Lead light curve with WD3")
        axWD1.plot(lightCurve_A['time'], lightCurve_A['dfWavDenoise_lcA'], linestyle='-', linewidth=1.3, color='black')
        # Plot the second DataFrame
        axWD1.errorbar(lightCurve_B['time'], lightCurve_B['dfWavDenoise_lcB'], yerr=lightCurve_B['lcB_WavErr'], fmt='s',
                       elinewidth=0.1, linewidth=0.1, markersize=2, color='magenta', label="Delayed light curve with WD3")
        axWD1.plot(lightCurve_B['time'], lightCurve_B['dfWavDenoise_lcB'], linestyle='-', linewidth=1.3, color='magenta')
        axWD1.set_xlabel("Time (days) continous form", fontsize=8)
        axWD1.set_ylabel("Lead lc offset 0.15, delayed lc offset 0.1, raw & denoised\nMagnitude", fontsize=6)
        #Change size of ticks for visual purposes
        axWD1.tick_params(axis="x", labelsize=6)
        axWD1.tick_params(axis="y", labelsize=6)
        axWD1.legend(fontsize="7")
        initial_canvas = FigureCanvasTkAgg(figWD3lc, master=framePlot_lcAB)
        canvas_widgetWD1 = initial_canvas.get_tk_widget()
        canvas_widgetWD1.grid(row=0, column=0, columnspan=1)
        # Adjust the Canvas widget's size to make the figure smalleror bigger-begin code to show histogram
        figWD3_A = plt.Figure(figsize=(2.5, 1.95))
        lcA_WD1_hst = figWD3_A.add_subplot(111)
        lcA_WD1_hst.hist(y_denoise, bins=10, alpha=0.5, color="blue", ec="black", lw=3)
        lcA_WD1_hst.set_title("Lead light curve with WD3", fontsize=8)  # Add title to histogram A
        lcA_WD1_hst.tick_params(axis="x", labelsize=6)
        lcA_WD1_hst.tick_params(axis="y", labelsize=6)

        figWD3_B = plt.Figure(figsize=(2.5, 1.95))
        lcB_WD1_hst = figWD3_B.add_subplot(111)
        lcB_WD1_hst.hist(y1_denoise, bins=10, alpha=0.5, color="#8B7B8B", ec="black", lw=3)  # 8B7B8B
        lcB_WD1_hst.set_title("Delayed light curve with WD3", fontsize=8)  # Add title to histogram A
        lcB_WD1_hst.tick_params(axis="x", labelsize=6)
        lcB_WD1_hst.tick_params(axis="y", labelsize=6)
        # Create a Frame to hold the widgets
        frameStatistical_A = tk.Frame(root)
        frameStatistical_B = tk.Frame(root)
        frameStatistical_A.grid(row=1, column=1, padx=3, pady=3)
        frameStatistical_B.grid(row=2, column=1, padx=3, pady=3)
        #
        canvasWD1lcA = FigureCanvasTkAgg(figWD3_A, master=frameStatistical_A)
        canvasWD1lcB = FigureCanvasTkAgg(figWD3_B, master=frameStatistical_B)
        #
        canvas_widgetWD1_A = canvasWD1lcA.get_tk_widget()
        canvas_widgetWD1_A.grid(row=0, column=0, columnspan=2)
        canvas_widgetWD1_B = canvasWD1lcB.get_tk_widget()
        canvas_widgetWD1_B.grid(row=0, column=0, columnspan=2)
        # Begin the descriptive statistics to the initial raw data apply the different techniques light curve A
        lcA_WD2 = pd.DataFrame(denoiseA_WD3)
        HurstA, c, data = compute_Hc(lcA_WD2, kind='random_walk', simplified=True)
        skewnessA = skew(lcA_WD2, axis=0, bias=True)
        curtosisA = kurtosis(lcA_WD2, axis=0, fisher=False, bias=True)
        resA, resB = stats.jarque_bera(lcA_WD2)
        resultA = adfuller(lcA_WD2)
        adfStatisticA = resultA[0]
        adfPvalueA = resultA[1]
        # Extract and print the critical values in a dictionary
        critical_values_dict = {key: value for key, value in resultA[4].items()}
        first_critical_valueA = critical_values_dict['1%']
        second_critical_valueA = critical_values_dict['5%']
        third_critical_valueA = critical_values_dict['10%']
        empty = ""
        statsA_WD3 = {
            'count': lcA_WD2.count().values[0],
            'mean': lcA_WD2.mean().values[0],
            'std.dev': lcA_WD2.std().values[0],
            'min': lcA_WD2.min().values[0],
            'max': lcA_WD2.max().values[0],
            'Hurst': HurstA,
            'Skewness': skewnessA,
            'Kurtosis': curtosisA,
            'Jarque-Bera': resA,
            'P-value': resB,
            'ADF-Statistic': adfStatisticA,
            'p-value': adfPvalueA,
            'Critical-Vals': empty,
            '1%:': first_critical_valueA,
            '5%:': second_critical_valueA,
            '10%:': third_critical_valueA
        }
        # Begin the descriptive statistics to the initial raw data apply the different techniques light curve B
        lcB_WD3 = pd.DataFrame(denoiseB_WD3)
        HurstB, c, data = compute_Hc(lcB_WD3, kind='random_walk', simplified=True)
        skewnessB = skew(lcB_WD3, axis=0, bias=True)
        curtosisB = kurtosis(lcB_WD3, axis=0, fisher=False, bias=True)
        resC, resD = stats.jarque_bera(lcB_WD3)
        resultB = adfuller(lcB_WD3)
        adfStatisticB = resultB[0]
        adfPvalueB = resultB[1]
        # Extract and print the critical values in a dictionary
        critical_values_dict = {key: value for key, value in resultA[4].items()}
        first_critical_valueB = critical_values_dict['1%']
        second_critical_valueB = critical_values_dict['5%']
        third_critical_valueB = critical_values_dict['10%']
        statsB_WD3 = {
            'count': lcB_WD3.count().values[0],
            'mean': lcB_WD3.mean().values[0],
            'std.dev': lcB_WD3.std().values[0],
            'min': lcB_WD3.min().values[0],
            'max': lcB_WD3.max().values[0],
            'Hurst': HurstB,
            'Skewness': skewnessB,
            'Kurtosis': curtosisB,
            'Jarque-Bera': resC,
            'p-value': resD,
            'ADF-Statistic': adfStatisticB,
            'P-value': adfPvalueB,
            'Critical-Vals': empty,
            '1%:': first_critical_valueB,
            '5%:': second_critical_valueB,
            '10%:': third_critical_valueB
        }
        # the descriptive statistic widget
        statisticalAnalysisA = tk.Text(frameStatistical_A, width=26, height=17, bg="#00CDCD",
                                       font=("Courier", 10))  # cyan3	#00CDCD	RGB(0,205,205)
        statisticalAnalysisA.grid(row=0, column=3, columnspan=1, padx=2, pady=2)

        statisticalAnalysisB = tk.Text(frameStatistical_B, width=26, height=17, bg="#7EC0EE",
                                       font=("Courier", 10))  # skyblue2 #7EC0EE RGB(126,192,238)
        statisticalAnalysisB.grid(row=0, column=3, columnspan=1, padx=2, pady=2)
        # Create a DataFrame with a single-row index for light curve A
        df_statsA = pd.DataFrame(statsA_WD3, index=['Statistics'])
        # Transpose the DataFrame
        df_statsA_transposed = df_statsA.transpose()
        # Convert the data in the second column to numeric and apply formatting-for only two decimal points
        column_name = 'Statistics'
        df_statsA_transposed[column_name] = pd.to_numeric(df_statsA_transposed[column_name], errors='coerce').apply(
            lambda x: f'{x:.2f}' if not pd.isnull(x) else '')
        # Get the formatted DataFrame as a string without the header and index
        statsA_str = df_statsA_transposed.to_string(header=False, index=False)
        # Create a list of lines with both column names and values
        lines = [f'{col:<18}{val}' if val else f'{col}' for col, val in
                 zip(df_statsA_transposed.index, statsA_str.split('\n'))]
        # Insert lines into the Text widget with line breaks
        formatted_output_WD3_lead = '\n'.join(lines)
        statisticalAnalysisA.insert(tk.END, formatted_output_WD3_lead)
        # Create a DataFrame with a single-row index for light curve B
        df_statsB = pd.DataFrame(statsB_WD3, index=['Statistics'])
        # Transpose the DataFrame
        df_statsB_transposed = df_statsB.transpose()
        # Convert the data in the second column to numeric and apply formatting-for only two decimal points
        column_nameB = 'Statistics'
        df_statsB_transposed[column_nameB] = pd.to_numeric(df_statsB_transposed[column_nameB], errors='coerce').apply(
            lambda x: f'{x:.2f}' if not pd.isnull(x) else '')
        # Get the formatted DataFrame as a string without the header and index
        statsB_str = df_statsB_transposed.to_string(header=False, index=False)
        # Create a list of lines with both column names and values
        linesB = [f'{col:<18}{val}' if val else f'{col}' for col, val in
                  zip(df_statsB_transposed.index, statsB_str.split('\n'))]
        # Insert lines into the Text widget with line breaks
        formatted_output_WD3_delay = '\n'.join(linesB)
        statisticalAnalysisB.insert(tk.END, formatted_output_WD3_delay)
        plt.show()
        colour1 = '#020f12'
        colour2 = '#DCDCDC'
        colour3 = '#C1CDC1'
        colour4 = '#292421'
        export_button = tk.Button(root, background=colour2, foreground=colour4, activebackground=colour3,
                           activeforeground=colour4, highlightthickness=4, highlightbackground=colour2,
                           highlightcolor='BLUE', width=28, height=1, border=2, cursor='hand1', font=('Arial', 13, 'bold'), text="Export descriptive statistics to PDF",
                    command = lambda: export_histogram_and_stats_to_pdf(
                    figures=[figWD3_A, figWD3_B],
                    stats_data=[formatted_output_WD3_lead, formatted_output_WD3_delay],
                    headers=['Descriptive Statistics for Lead Light Curve with WD3', 'Descriptive Statistics for Delayed Light Curve with WD3'],
                    additional_figure=figWD3lc,
                    additional_header="Light Curves with Raw Data and Wavelet Denoise lvl 3",
                    initial_dir =os.path.expanduser('~'),
                    initial_file ="Plot_and_Statistics_WD_level3.pdf"
                    ))
        export_button.grid(row=0, column=1, pady=10)

    elif preprocessing_selectionSA == "Christiano-Fitzgerald filter":
        # Remove the frame and canvas from the grid layout
        if frameStatistical_A:
            frameStatistical_A.grid_forget()
        if frameStatistical_B:
            frameStatistical_B.grid_forget()

        dfA_CF = series_data[1].copy()
        dfB_CF = series_data[2].copy()
        # Rename the columns
        dfA_CF.rename(columns={"Julian_day": "time", "Magnitude": "lc_A", "error": "error_A"}, inplace=True)
        dfA_CF['pctErr_A'] = dfA_CF['error_A'] / dfA_CF['lc_A']
        dfB_CF.rename(columns={"Julian_day": "time", "Magnitude": "lc_B", "error": "error_B"}, inplace=True)
        dfB_CF['pctErr_B'] = dfB_CF['error_B'] / dfB_CF['lc_B']
        time = dfA_CF['time']
        # Convert both time series to numpy to apply the CF filter
        df_lcA_numpy = dfA_CF['lc_A'].to_numpy()
        df_lcA_numpy.flatten()
        df_lcB_numpy = dfB_CF['lc_B'].to_numpy()
        df_lcB_numpy.flatten()
        # Apply the CF filter algorithm to both light curves
        cycleA, trendA = sm.tsa.filters.cffilter(df_lcA_numpy, 6, 32, drift=False)
        cycleB, trendB = sm.tsa.filters.cffilter(df_lcB_numpy, 6, 32, drift=False)
        # Converting the CF cycle and trend numpy array (light curve A) to a dataframe column
        dfCycle_lcA = pd.DataFrame(cycleA)
        dfTrend_lcA = pd.DataFrame(trendA)
        # Converting the CF cycle and trend numpy array (light curve B) to a dataframe column
        dfCycle_lcB = pd.DataFrame(cycleB)
        dfTrend_lcB = pd.DataFrame(trendB)

        dfCycle_lcA = dfCycle_lcA.to_numpy().flatten()
        dfTrend_lcA = dfTrend_lcA.to_numpy().flatten()
        dfCycle_lcB = dfCycle_lcB.to_numpy().flatten()
        dfTrend_lcB = dfTrend_lcB.to_numpy().flatten()
        # calculating the error for light curve A
        dfCycle_lcA_Err = abs(dfCycle_lcA * dfA_CF['pctErr_A'])
        dfTrend_lcA_Err = abs(dfTrend_lcA * dfA_CF['pctErr_A'])
        # calculating the error for light curve B
        dfCycle_lcB_Err = abs(dfCycle_lcB * dfB_CF['pctErr_B'])
        dfTrend_lcB_Err = abs(dfTrend_lcB * dfB_CF['pctErr_B'])

        lightCurve_A_cycle = {
            'time': time,
            'dfCycle_lcA': dfCycle_lcA,
            'dfCycle_lcA_Err': dfCycle_lcA_Err,
        }
        lightCurve_B_cycle = {
            'time': time,
            'dfCycle_lcB': dfCycle_lcB,
            'dfCycle_lcB_Err': dfCycle_lcB_Err,
        }
        # CF trend
        lightCurve_A_trend = {
            'time': time,
            'dfTrend_lcA': dfTrend_lcA,
            'dfTrend_lcA_Err': dfTrend_lcA_Err,
        }

        lightCurve_B_trend = {
            'time': time,
            'dfTrend_lcB': dfTrend_lcB,
            'dfTrend_lcB_Err': dfTrend_lcB_Err,
        }
        # Begin the code for plot the light curves A and B and to adjust the figsize to decrease or increase the size of the graphic
        figCF = plt.Figure(figsize=(4.7, 2.65))
        axCF = figCF.add_subplot(111)
        # ax.set_position is [left, bottom, width, height] by increasing the third an fourth parameter
        axCF.set_position([0.11, 0.1585, 0.85, 0.83])
        # Plot the first DataFrame
        axCF.errorbar(lightCurve_A_trend['time'], lightCurve_A_trend['dfTrend_lcA'],
                      yerr=lightCurve_A_trend['dfTrend_lcA_Err'], fmt='s', elinewidth=0.5, markersize=1,
                      label="Lead light curve-CF trend")
        axCF.errorbar(lightCurve_A_cycle['time'], lightCurve_A_cycle['dfCycle_lcA'],
                      yerr=lightCurve_A_cycle['dfCycle_lcA_Err'], fmt='s', elinewidth=0.5, markersize=1,
                      label="Lead light curve-CF cycle")
        # Plot the second DataFrame
        axCF.errorbar(lightCurve_B_trend['time'], lightCurve_B_trend['dfTrend_lcB'],
                      yerr=lightCurve_B_trend['dfTrend_lcB_Err'], fmt='s', elinewidth=0.5, markersize=1,
                      label="Delayed light curve-CF trend")
        axCF.errorbar(lightCurve_B_cycle['time'], lightCurve_B_cycle['dfCycle_lcB'],
                      yerr=lightCurve_B_cycle['dfCycle_lcB_Err'], fmt='s', elinewidth=0.5, markersize=1,
                      label="Delayed light curve-CF cycle")
        axCF.set_xlabel("Time (days)", fontsize=8)
        axCF.set_ylabel("Magnitude", fontsize=8)
        axCF.tick_params(axis="x", labelsize=6)
        axCF.tick_params(axis="y", labelsize=6)
        axCF.legend(fontsize="7")
        # Initialize canvas
        initial_canvas = FigureCanvasTkAgg(figCF, master=framePlot_lcAB)
        canvas_widgetCF = initial_canvas.get_tk_widget()
        canvas_widgetCF.grid(row=0, column=0, columnspan=1)
        ##################Begin the histogram code for CF trend
        figCFtrend_A = plt.Figure(figsize=(2.1, 1.95))
        lcA_CFtrend_hst = figCFtrend_A.add_subplot(111)
        # Set size for histogram for light curve A
        lcA_CFtrend_hst.hist(dfTrend_lcA, bins=10, alpha=0.5, color="blue", ec="black", lw=3)
        lcA_CFtrend_hst.set_title("Lead light curve A in CF trend", fontsize=8)  # Add title to histogram A
        # Set size for ticks labels for light curve A
        lcA_CFtrend_hst.tick_params(axis="x", labelsize=6)
        lcA_CFtrend_hst.tick_params(axis="y", labelsize=6)
        # Set size for histogram for light curve B
        figCFtrend_B = plt.Figure(figsize=(2.1, 1.95))
        lcB_CFtrend_hst = figCFtrend_B.add_subplot(111)

        lcB_CFtrend_hst.hist(dfTrend_lcB, bins=10, alpha=0.5, color="#8B7B8B", ec="black", lw=3)  # thistle4	#8B7B8B	RGB(139,123,139)
        lcB_CFtrend_hst.set_title("Delayed light curve in CF trend", fontsize=8)  # Add title to histogram A
        # Set size for ticks labels for light curve A
        lcB_CFtrend_hst.tick_params(axis="x", labelsize=6)
        lcB_CFtrend_hst.tick_params(axis="y", labelsize=6)
        # Create a Frame to hold the widgets
        frameStatistical_A = tk.Frame(root)
        frameStatistical_B = tk.Frame(root)
        frameStatistical_A.grid(row=1, column=1, padx=3, pady=3)
        frameStatistical_B.grid(row=2, column=1, padx=3, pady=3)
        #
        canvasCFtrendlcA = FigureCanvasTkAgg(figCFtrend_A, master=frameStatistical_A)
        canvasCFtrendlcB = FigureCanvasTkAgg(figCFtrend_B, master=frameStatistical_B)
        #
        canvas_widgetCFtrend_A = canvasCFtrendlcA.get_tk_widget()
        canvas_widgetCFtrend_A.grid(row=0, column=0, columnspan=2)

        canvas_widgetCFtrend_B = canvasCFtrendlcB.get_tk_widget()
        canvas_widgetCFtrend_B.grid(row=0, column=0, columnspan=2)
        # Begin the descriptive statistics to the initial raw data apply the different techniques light curve A CF trend
        lcA_CFtrend = pd.DataFrame(dfTrend_lcA)
        HurstA, c, data = compute_Hc(lcA_CFtrend, kind='random_walk', simplified=True)
        skewnessA = skew(lcA_CFtrend, axis=0, bias=True)
        curtosisA = kurtosis(lcA_CFtrend, axis=0, fisher=False, bias=True)
        resA, resB = stats.jarque_bera(lcA_CFtrend)
        resultA = adfuller(lcA_CFtrend)
        adfStatisticA = resultA[0]
        adfPvalueA = resultA[1]
        # Extract and print the critical values in a dictionary
        critical_values_dict = {key: value for key, value in resultA[4].items()}
        first_critical_valueA = critical_values_dict['1%']
        second_critical_valueA = critical_values_dict['5%']
        third_critical_valueA = critical_values_dict['10%']
        empty = ""
        statsA_CFtrend = {
            'count': lcA_CFtrend.count().values[0],
            'mean': lcA_CFtrend.mean().values[0],
            'std.dev': lcA_CFtrend.std().values[0],
            'min': lcA_CFtrend.min().values[0],
            'max': lcA_CFtrend.max().values[0],
            'Hurst': HurstA,
            'Skewness': skewnessA,
            'Kurtosis': curtosisA,
            'Jarque-Bera': resA,
            'P-value': resB,
            'ADF-Statistic': adfStatisticA,
            'p-value': adfPvalueA,
            'Critical-Vals': empty,
            '1%:': first_critical_valueA,
            '5%:': second_critical_valueA,
            '10%:': third_critical_valueA
        }
        # Begin the descriptive statistics to the initial raw data apply the different techniques light curve B
        lcB_CFtrend = pd.DataFrame(dfTrend_lcB)
        HurstB, c, data = compute_Hc(lcB_CFtrend, kind='random_walk', simplified=True)
        skewnessB = skew(lcB_CFtrend, axis=0, bias=True)
        curtosisB = kurtosis(lcB_CFtrend, axis=0, fisher=False, bias=True)
        resC, resD = stats.jarque_bera(lcB_CFtrend)
        resultB = adfuller(lcB_CFtrend)
        adfStatisticB = resultB[0]
        adfPvalueB = resultB[1]
        # Extract and print the critical values in a dictionary
        critical_values_dict = {key: value for key, value in resultA[4].items()}
        first_critical_valueB = critical_values_dict['1%']
        second_critical_valueB = critical_values_dict['5%']
        third_critical_valueB = critical_values_dict['10%']
        statsB_CFtrend = {
            'count': lcB_CFtrend.count().values[0],
            'mean': lcB_CFtrend.mean().values[0],
            'std.dev': lcB_CFtrend.std().values[0],
            'min': lcB_CFtrend.min().values[0],
            'max': lcB_CFtrend.max().values[0],
            'Hurst': HurstB,
            'Skewness': skewnessB,
            'Kurtosis': curtosisB,
            'Jarque-Bera': resC,
            'P-value': resD,
            'ADF-Statistic': adfStatisticB,
            'p-value': adfPvalueB,
            'Critical-Vals': empty,
            '1%:': first_critical_valueB,
            '5%:': second_critical_valueB,
            '10%:': third_critical_valueB
        }
        # the descriptive statistic widget
        statisticalAnalysisA = tk.Text(frameStatistical_A, width=26, height=17, bg="cyan3", font=("Courier", 10))
        statisticalAnalysisA.grid(row=0, column=3, columnspan=1, padx=2, pady=2)
        statisticalAnalysisB = tk.Text(frameStatistical_B, width=26, height=17, bg="#00CDCD",
                                       font=("Courier", 10))  # cyan3	#00CDCD	RGB(0,205,205)
        statisticalAnalysisB.grid(row=0, column=3, columnspan=1, padx=2, pady=2)
        # Create a DataFrame with a single-row index for light curve A
        df_statsA = pd.DataFrame(statsA_CFtrend, index=['Statistics'])
        # Transpose the DataFrame
        df_statsA_transposed = df_statsA.transpose()
        # Convert the data in the second column to numeric and apply formatting-for only two decimal points
        column_name = 'Statistics'
        df_statsA_transposed[column_name] = pd.to_numeric(df_statsA_transposed[column_name], errors='coerce').apply(
            lambda x: f'{x:.2f}' if not pd.isnull(x) else '')
        # Get the formatted DataFrame as a string without the header and index
        statsA_str = df_statsA_transposed.to_string(header=False, index=False)
        # Create a list of lines with both column names and values
        lines = [f'{col:<18}{val}' if val else f'{col}' for col, val in
                 zip(df_statsA_transposed.index, statsA_str.split('\n'))]
        # Insert lines into the Text widget with line breaks
        formatted_output_lead_CF_trend = '\n'.join(lines)
        statisticalAnalysisA.insert(tk.END, formatted_output_lead_CF_trend)
        # Create a DataFrame with a single-row index for light curve B
        df_statsB = pd.DataFrame(statsB_CFtrend, index=['Statistics'])
        # Transpose the DataFrame
        df_statsB_transposed = df_statsB.transpose()
        # Convert the data in the second column to numeric and apply formatting-for only two decimal points
        column_nameB = 'Statistics'
        df_statsB_transposed[column_nameB] = pd.to_numeric(df_statsB_transposed[column_nameB], errors='coerce').apply(
            lambda x: f'{x:.2f}' if not pd.isnull(x) else '')
        # Get the formatted DataFrame as a string without the header and index
        statsB_str = df_statsB_transposed.to_string(header=False, index=False)
        # Create a list of lines with both column names and values
        linesB = [f'{col:<18}{val}' if val else f'{col}' for col, val in
                  zip(df_statsB_transposed.index, statsB_str.split('\n'))]
        # Insert lines into the Text widget with line breaks
        formatted_output_delayed_CF_trend = '\n'.join(linesB)
        statisticalAnalysisB.insert(tk.END, formatted_output_delayed_CF_trend)
        ##################Begin the histogram code for CF cycle
        # Set size for CF-cycle histogram for light curve
        figCFcycle_A = plt.Figure(figsize=(2.1, 1.95))
        lcA_CFcycle_hst = figCFcycle_A.add_subplot(111)

        lcA_CFcycle_hst.hist(dfCycle_lcA, bins=10, alpha=0.5, color="blue", ec="black", lw=3)
        lcA_CFcycle_hst.set_title("Lead light curve in CF cycle", fontsize=8)  # Add title to histogram A
        # Set size for ticks labels for light curve A
        lcA_CFcycle_hst.tick_params(axis="x", labelsize=6)
        lcA_CFcycle_hst.tick_params(axis="y", labelsize=6)
        # Set size for CF-cycle histogram for light curve B
        figCFcycle_B = plt.Figure(figsize=(2.1, 1.95))
        lcB_CFcycle_hst = figCFcycle_B.add_subplot(111)

        lcB_CFcycle_hst.hist(dfCycle_lcB, bins=10, alpha=0.5, color="#8B7B8B", ec="black",
                             lw=3)  # thistle4	#8B7B8B	RGB(139,123,139)
        lcB_CFcycle_hst.set_title("Delayed light curve in CF cycle", fontsize=8)  # Add title to histogram A
        # Set size for ticks labels for light curve A
        lcB_CFcycle_hst.tick_params(axis="x", labelsize=6)
        lcB_CFcycle_hst.tick_params(axis="y", labelsize=6)
        # Create a Frame to hold the widgets
        frameStatistical_A = tk.Frame(root)
        frameStatistical_B = tk.Frame(root)
        frameStatistical_A.grid(row=1, column=4, padx=1, pady=1)
        frameStatistical_B.grid(row=2, column=4, padx=1, pady=1)
        #
        canvasCFcyclelcA = FigureCanvasTkAgg(figCFcycle_A, master=frameStatistical_A)
        canvasCFcyclelcB = FigureCanvasTkAgg(figCFcycle_B, master=frameStatistical_B)
        #
        canvas_widgetCFtrend_A = canvasCFcyclelcA.get_tk_widget()
        canvas_widgetCFtrend_A.grid(row=0, column=0, columnspan=2)

        canvas_widgetCFcycle_B = canvasCFcyclelcB.get_tk_widget()
        canvas_widgetCFcycle_B.grid(row=0, column=0, columnspan=2)
        # Begin the descriptive statistics to the initial raw data apply the different techniques light curve A CF cycle
        lcA_CFcycle = pd.DataFrame(dfCycle_lcA)
        HurstA, c, data = compute_Hc(lcA_CFcycle, kind='random_walk', simplified=True)
        skewnessA = skew(lcA_CFcycle, axis=0, bias=True)
        curtosisA = kurtosis(lcA_CFcycle, axis=0, fisher=False, bias=True)
        resA, resB = stats.jarque_bera(lcA_CFcycle)
        resultA = adfuller(lcA_CFcycle)
        adfStatisticA = resultA[0]
        adfPvalueA = resultA[1]
        # Extract and print the critical values in a dictionary
        critical_values_dict = {key: value for key, value in resultA[4].items()}
        first_critical_valueA = critical_values_dict['1%']
        second_critical_valueA = critical_values_dict['5%']
        third_critical_valueA = critical_values_dict['10%']
        empty = ""
        statsA_CFcycle = {
            'count': lcA_CFcycle.count().values[0],
            'mean': lcA_CFcycle.mean().values[0],
            'std.dev': lcA_CFcycle.std().values[0],
            'min': lcA_CFcycle.min().values[0],
            'max': lcA_CFcycle.max().values[0],
            'Hurst': HurstA,
            'Skewness': skewnessA,
            'Kurtosis': curtosisA,
            'Jarque-Bera': resA,
            'P-value': resB,
            'ADF-Statistic': adfStatisticA,
            'p-value': adfPvalueA,
            'Critical-Vals': empty,
            '1%:': first_critical_valueA,
            '5%:': second_critical_valueA,
            '10%:': third_critical_valueA
        }
        # Begin the descriptive statistics to the initial raw data apply the different techniques light curve B
        lcB_CFcycle = pd.DataFrame(dfCycle_lcB)
        HurstB, c, data = compute_Hc(lcB_CFcycle, kind='random_walk', simplified=True)
        skewnessB = skew(lcB_CFcycle, axis=0, bias=True)
        curtosisB = kurtosis(lcB_CFcycle, axis=0, fisher=False, bias=True)
        resC, resD = stats.jarque_bera(lcB_CFcycle)
        resultB = adfuller(lcB_CFcycle)
        adfStatisticB = resultB[0]
        adfPvalueB = resultB[1]
        # Extract and print the critical values in a dictionary
        critical_values_dict = {key: value for key, value in resultA[4].items()}
        first_critical_valueB = critical_values_dict['1%']
        second_critical_valueB = critical_values_dict['5%']
        third_critical_valueB = critical_values_dict['10%']
        statsB_CFcycle = {
            'count': lcB_CFcycle.count().values[0],
            'mean': lcB_CFcycle.mean().values[0],
            'std.dev': lcB_CFcycle.std().values[0],
            'min': lcB_CFcycle.min().values[0],
            'max': lcB_CFcycle.max().values[0],
            'Hurst': HurstB,
            'Skewness': skewnessB,
            'Kurtosis': curtosisB,
            'Jarque-Bera': resC,
            'P-value': resD,
            'ADF-Statistic': adfStatisticB,
            'p-value': adfPvalueB,
            'Critical-Vals': empty,
            '1%:': first_critical_valueB,
            '5%:': second_critical_valueB,
            '10%:': third_critical_valueB }
        # the descriptive statistic widget
        statisticalAnalysisA = tk.Text(frameStatistical_A, width=26, height=17, bg="#7EC0EE", font=("Courier", 10))
        statisticalAnalysisA.grid(row=0, column=3, columnspan=1, padx=2, pady=2)

        statisticalAnalysisB = tk.Text(frameStatistical_B, width=26, height=17, bg="#7EC0EE",
                                       font=("Courier", 10))  # skyblue2	#7EC0EE	RGB(126,192,238)
        statisticalAnalysisB.grid(row=0, column=3, columnspan=1, padx=2, pady=2)
        # Create a DataFrame with a single-row index for light curve A
        df_statsA = pd.DataFrame(statsA_CFcycle, index=['Statistics'])
        # Transpose the DataFrame
        df_statsA_transposed = df_statsA.transpose()
        # Convert the data in the second column to numeric and apply formatting-for only two decimal points
        column_name = 'Statistics'
        df_statsA_transposed[column_name] = pd.to_numeric(df_statsA_transposed[column_name], errors='coerce').apply(
            lambda x: f'{x:.2f}' if not pd.isnull(x) else '')
        # Get the formatted DataFrame as a string without the header and index
        statsA_str = df_statsA_transposed.to_string(header=False, index=False)
        # Create a list of lines with both column names and values
        lines = [f'{col:<18}{val}' if val else f'{col}' for col, val in
                 zip(df_statsA_transposed.index, statsA_str.split('\n'))]
        # Insert lines into the Text widget with line breaks
        formatted_output_lead_CF_cycle = '\n'.join(lines)
        statisticalAnalysisA.insert(tk.END, formatted_output_lead_CF_cycle)
        # Create a DataFrame with a single-row index for light curve B
        df_statsB = pd.DataFrame(statsB_CFcycle, index=['Statistics'])
        # Transpose the DataFrame
        df_statsB_transposed = df_statsB.transpose()
        # Convert the data in the second column to numeric and apply formatting-for only two decimal points
        column_nameB = 'Statistics'
        df_statsB_transposed[column_nameB] = pd.to_numeric(df_statsB_transposed[column_nameB], errors='coerce').apply(
            lambda x: f'{x:.2f}' if not pd.isnull(x) else '')
        # Get the formatted DataFrame as a string without the header and index
        statsB_str = df_statsB_transposed.to_string(header=False, index=False)
        # Create a list of lines with both column names and values
        linesB = [f'{col:<18}{val}' if val else f'{col}' for col, val in
                  zip(df_statsB_transposed.index, statsB_str.split('\n'))]
        # Insert lines into the Text widget with line breaks
        formatted_output_delayed_CF_cycle = '\n'.join(linesB)
        # Insert text with the tag applied
        statisticalAnalysisB.insert(tk.END, formatted_output_delayed_CF_cycle)
        plt.show()
        colour1 = '#020f12'
        colour2 = '#DCDCDC'
        colour3 = '#C1CDC1'
        colour4 = '#292421'
        export_button = tk.Button(root, background=colour2, foreground=colour4, activebackground=colour3,
                          activeforeground=colour4, highlightthickness=4, highlightbackground=colour2,
                          highlightcolor='BLUE', width=28, height=1, border=2, cursor='hand1',
                          font=('Arial', 13, 'bold'), text="Export descriptive statistics to PDF",
                          command=export_both_statistics)  # Set the wrapper function as the command
        export_button.grid(row=0, column=1, pady=10)
        ##########End of function
def export_both_statistics():
    """
    Exports statistical analysis and histograms to PDF files. This function generates two PDF reports:
    one for the CF-cycle data and another for the CF-trend data. Each report includes histograms of the lead
    and delayed light curves along with their descriptive statistics.

    Global Variables:
    - figCFcycle_A, figCFcycle_B: Matplotlib figures for the CF-cycle histograms.
    - formatted_output_lead_CF_cycle, formatted_output_delayed_CF_cycle: Strings containing descriptive statistics for CF-cycle.
    - figCFtrend_A, figCFtrend_B: Matplotlib figures for the CF-trend histograms.
    - formatted_output_lead_CF_trend, formatted_output_delayed_CF_trend: Strings containing descriptive statistics for CF-trend.
    - figCF: An additional figure that might be used in the report.

    The function makes two separate calls to `export_histogram_and_stats_to_pdf` with different parameters
    to generate the two reports. Each report contains the histograms, descriptive statistics, and an optional
    additional figure if provided.

    Parameters for `export_histogram_and_stats_to_pdf` include:
    - figures: A list of matplotlib figure objects to be included in the report.
    - stats_data: A list of strings containing descriptive statistics.
    - headers: A list of headers for each section of the report.
    - additional_figure: An optional matplotlib figure object to be included at the end of the report.
    - initial_dir: Directory to open the save dialog in.
    - initial_file: Default name for the saved PDF file.
    """
    # First call to export function
    global figCFcycle_A
    global figCFcycle_B
    global formatted_output_lead_CF_cycle
    global formatted_output_delayed_CF_cycle
    global figCFtrend_A
    global figCFtrend_B
    global formatted_output_lead_CF_trend
    global formatted_output_delayed_CF_trend
    global figCF
    export_histogram_and_stats_to_pdf(
        figures=[figCFcycle_A, figCFcycle_B],
        stats_data=[formatted_output_lead_CF_cycle, formatted_output_delayed_CF_cycle],
        headers=[
            'Descriptive Statistics for Lead Light Curve in CF-cycle',
            'Descriptive Statistics for Delayed Light Curve in CF-cycle'
        ],
        additional_figure=figCF,
        additional_header="Light Curves with CF-cycle and CF-trend",
        initial_dir=os.path.expanduser('~'),
        initial_file="Plot_and_Statistics_CF-cycle.pdf"
    )
    # Second call to export function with different parameters
    export_histogram_and_stats_to_pdf(
        figures=[figCFtrend_A, figCFtrend_B],  # Use different figures for the second call
        stats_data=[formatted_output_lead_CF_trend, formatted_output_delayed_CF_trend],
        headers=[
            'Descriptive Statistics for Lead Light Curve in CF-trend',
            'Descriptive Statistics for Delayed Light Curve in CF-trend'
        ],
        additional_figure=figCF,  # additional figure
        additional_header="Light Curves with CF-cycle and CF-trend",
        initial_dir=os.path.expanduser('~'),
        initial_file="Plot_and_Statistics_CF-trend.pdf"
    )

def enable_entryTrueDelayBox():
    """
    Enables the entry box for direct input of the true or guessed time delay and disables the range search combobox.
    This function is typically bound to a radio button selection indicating the user's choice to input a specific
    delay value directly.
    """
    delayEntry.config(state='normal')
    timeDelay_range_search.config(state='disabled')
    delayLabel.config(text="Insert true or guess delay")

def enable_SearchRange_combobox():
    """
    Enables the combobox for selecting a range of search for the time delay and disables the direct input entry box.
    This function is typically bound to a radio button selection indicating the user's choice to select a delay
    range from predefined options.
    """
    timeDelay_range_search.config(state='normal')
    delayEntry.config(state='disabled')
    delayLabel.config(text="Choose a range of search")
# This function update the value in the dictionary for global variables
def update_global_vars():
    """
    Updates the `global_vars` dictionary with the current selections and results from the delay estimation process.
    This function consolidates the latest application state into a single global dictionary, making it accessible
    for other operations such as exporting results.

    Updates include:
    - preprocessing selection,
    - delay estimation method selection,
    - any generated results from the delay estimation processes.
    """
    global global_vars
    global_vars = {
        'preprocessing_selectionAA': preprocessing_selectionAA,
        'delayMethod_selectionAA': delayMethod_selectionAA,
        'banderaKnownDelay': banderaKnownDelay,
        'banderaSearchRange': banderaSearchRange,
        'filteredRawData': filteredRawData,
        'filteredDiffData': filteredDiffData,
        'DSv1RawData_SearchRange': DSv1RawData_SearchRange,
        'DSv1DiffData_SearchRange': DSv1DiffData_SearchRange,
    'filteredSNR_Data': filteredSNR_Data,
    'DSv1SNR_Data_SearchRange': DSv1SNR_Data_SearchRange,
    'filteredWD_Data': filteredWD_Data,
    'DSv1WD_Data_SearchRange': DSv1WD_Data_SearchRange,
    'filteredWD2_Data': filteredWD2_Data,
    'DSv1WD2_Data_SearchRange': DSv1WD2_Data_SearchRange,
    'filteredWD3_Data': filteredWD3_Data,
    'DSv1WD3_Data_SearchRange': DSv1WD3_Data_SearchRange,
    'filteredWD3_Data': filteredWD3_Data,
    'DSv1WD3_Data_SearchRange': DSv1WD3_Data_SearchRange,
     'filteredCycle': filteredCycle,
     'filteredTrend': filteredTrend,
    'combined_df_CF_KD': combined_df_CF_KD,
     'combined_df_CF_SR': combined_df_CF_SR,
     'LNDCF_RawData_KD':  LNDCF_RawData_KD,
    'LNDCF_RawData_SR':  LNDCF_RawData_SR,
    'LNDCF_DiffData': LNDCF_DiffData,
     'LNDCF_DiffData_SR': LNDCF_DiffData_SR,
     'LNDCF_SNR_Data': LNDCF_SNR_Data,
     'LNDCF_SNR_Data_SR': LNDCF_SNR_Data_SR,
     'LNDCF_CFcycle_Data': LNDCF_CFcycle_Data,
     'LNDCF_CFtrend_Data': LNDCF_CFtrend_Data,
     'combined_df_LNDCF_CF_KD': combined_df_LNDCF_CF_KD,
      'combined_df_LNDCF_CF_SR': combined_df_LNDCF_CF_SR,
     'LNDCF_WD1_SR': LNDCF_WD1_SR,
     'LNDCF_WD1_KD': LNDCF_WD1_KD,
     'LNDCF_WD2_SR': LNDCF_WD2_SR,
     'LNDCF_WD2_KD': LNDCF_WD2_KD,
     'LNDCF_WD3_SR': LNDCF_WD3_SR,
     'LNDCF_WD3_KD': LNDCF_WD3_KD,
     'DCF_RawData': DCF_RawData,
     'DCF_RawData_SR': DCF_RawData_SR,
     'DCF_DiffData_SR': DCF_DiffData_SR,
     'DCF_DiffData': DCF_DiffData,
     'DCF_SNR_Data': DCF_SNR_Data,
     'DCF_SNR_Data_SR': DCF_SNR_Data_SR,
     'DCF_CFcycle_Data': DCF_CFcycle_Data,
     'DCF_CFtrend_Data': DCF_CFtrend_Data,
     'combined_df_DCF_SR': combined_df_DCF_SR,
     'combined_df_DFC_KD': combined_df_DFC_KD,
     'DCF_WD1_KD': DCF_WD1_KD,
     'DCF_WD1_SR': DCF_WD1_SR,
     'DCF_WD2_KD': DCF_WD2_KD,
     'DCF_WD2_SR': DCF_WD2_SR,
     'DCF_WD3_KD': DCF_WD3_KD,
     'DCF_WD3_SR': DCF_WD3_SR
    }

# Trough this function is called an external function to save the results in a csv file
def save_button_command():
    """
    Invokes the process to save the current results to a CSV file when the 'Save delay results to CSV' button is clicked.
    This function first updates the `global_vars` dictionary to ensure it contains the latest application state and
    results, then calls `determine_and_save_csv` to prompt the user for a file location and save the results.

    Note:
    - `determine_and_save_csv` is expected to use `global_vars` to determine which results to save and handle the file
      writing operation.
    """
    update_global_vars()  # Ensure global_vars has the latest values
    global global_vars  # Declare global_vars as global
    global_vars = determine_and_save_csv(global_vars)

###########################################################
set_font1 = Font(family="Helvetica", size=12, weight="bold")
set_font2 = Font(family="Helvetica", size=11)
# Create a Style object
style = ttk.Style()

# Create a Frame to hold the widgets
frameUpper = tk.Frame(root, width=180, height=100, bg="#E5E5E5")  # gray90	#E5E5E5	RGB(229,229,229)
frameUpper.grid(row=0, column=0, padx=3, pady=3)

frameMidOptions = tk.Frame(root, bg="#DCDCDC")#gainsboro #DCDCDC RGB(220,220,220)
frameMidOptions.grid(row=2, column=0, padx=3, pady=3)
# Configure the Combobox style with a larger font size
style.configure('TCombobox', font=('Helvetica', 12))
root.option_add("*TCombobox*Listbox.font", "Calibri 12")
root.option_add('*TCombobox*Listbox.foreground', 'blue')
# Create buttons for uploading time series and displaying both

upload_button1 = tk.Button(frameUpper, text="Upload lead light curve", font=set_font1, command=lambda: upload_file(1))
upload_button1.grid(row=0, column=0, padx=1, pady=1)

upload_button2 = tk.Button(frameUpper, text="Upload delayed light curve", font= set_font1, command=lambda: upload_file(2))
upload_button2.grid(row=0, column=1, padx=1, pady=1)

display_StatisticaAn_button = tk.Button(frameUpper, text="Descriptive statistics\n& Light curves plot", font= set_font1, command=display_statistical_analysis)
display_StatisticaAn_button.grid(row=0, column=2, padx=5, pady=5)
# Add labels to the selection comboboxes
#choosePreprocessingLabel = ttk.Label(frameMidOptions, font= set_font2, text="Choose a preproccesing technique")
#choosePreprocessingLabel.grid(row=4, column=0, sticky='W')

# Adjust column configuration to prevent expanding
frameMidOptions.columnconfigure(0, weight=0)

# Label with minimal horizontal padding
choosePreprocessingLabel = ttk.Label(frameMidOptions, font=set_font2, text="Choose a preprocessing technique")
choosePreprocessingLabel.grid(row=4, column=0, sticky='W', padx=(0, 5))  # Adjust padx as needed

chooseTimeDelayMethodLabel = ttk.Label(frameMidOptions, font= set_font2, text="Select a delay estimation method")
chooseTimeDelayMethodLabel.grid(row=4, column=1, sticky='E')
# Combo box - Group 1 prepocessing technique selection
preprocessing_selection = tk.StringVar()

preprocessing_method = ttk.Combobox(frameMidOptions, font= set_font2, textvariable=preprocessing_selection, width=22)
preprocessing_method["values"] = (
"Raw Data", "Data Differencing", "Simple Net Return", "Christiano-Fitzgerald filter", "Wavelet Denoise lvl 1",
"Wavelet Denoise lvl 2", "Wavelet Denoise lvl 3")
preprocessing_method["state"] = "readonly"
preprocessing_method.grid(row=5, column=0, padx=15, pady=15)
preprocessing_method.set("Select item")
# Combo box  - Group 2 time delay estimation method selection
delayMethod_selection = tk.StringVar()

timeDelay_methods = ttk.Combobox(frameMidOptions, font= set_font2, textvariable=delayMethod_selection, width=29)
timeDelay_methods["values"] = ("Dispersion Spectra", "Locally Normalized DCF", "Discrete Correlation Function (DCF)")
timeDelay_methods["state"] = "readonly"
timeDelay_methods.grid(row=5, column=1, padx=5, pady=5, sticky='W')
timeDelay_methods.set("Select item")
# Label to display value
delayLabel = ttk.Label(frameMidOptions, font= set_font2, text="Insert true or guess delay")
delayLabel.grid(row=6, column=0, sticky='W')
# Create and configure the radio buttons
radioButon_Selection = IntVar()
yes_radio = tk.Radiobutton(frameMidOptions, font= set_font2, text="Yes", variable=radioButon_Selection, value=1, command=enable_entryTrueDelayBox)
no_radio = tk.Radiobutton(frameMidOptions, font= set_font2, text="No", variable=radioButon_Selection, value=2, command=enable_SearchRange_combobox)
yes_radio.grid(row=6, column=1, padx=1, sticky='W')
no_radio.grid(row=6, column=1, padx=1, sticky='N')
radioButon_Selection.set(2)
# Combobox to determine the range of time delay
timeDelay_range_search = ttk.Combobox(frameMidOptions, font= set_font2, state='disabled', width=13)
timeDelay_range_search["values"] = (
"1 to 20", "20 to 40", "40 to 60", "60 to 80", "80 to 100", "100 to 120", "120 to 140", "140 to 160", "160 to 180",
"180 to 200", "200 to 220", "220 to 240", "240 to 260", "260 to 280", "280 to 300", "300 to 320", "320 to 340",
"340 to 360", "360 to 380", "380 to 400", "400 to 420", "420 to 440")
timeDelay_range_search["state"] = "readonly"
timeDelay_range_search.grid(row=7, column=1, padx=10, pady=5, sticky='N')
timeDelay_range_search.set("Select range")
# Display results button
colour1 = '#020f12'
colour2 = '#DCDCDC'
colour3 = '#C1CDC1'
colour4 = '#292421'
results_button = tk.Button(frameMidOptions, background=colour2, foreground=colour4, activebackground=colour3,
                           activeforeground=colour4, highlightthickness=4, highlightbackground=colour2,
                           highlightcolor='BLUE', width=11, height=2, border=2, cursor='hand1', font=('Arial', 14, 'bold'),
                           text="Display time \ndelay results", command=display_results)
results_button.grid(row=7, column=2, columnspan=2, padx=11, pady=2, sticky='W')
# save an output csv file results to hard disk
save_button = tk.Button(frameMidOptions, background=colour2, foreground=colour4, activebackground=colour3,
                           activeforeground=colour4, highlightthickness=4, highlightbackground=colour2,
                           highlightcolor='BLUE', width=11, height=2, border=2, cursor='hand1', font=('Arial', 13, 'bold'),
                           text="Save delay\nresults to CSV", command=save_button_command)
save_button.grid(row=5, column=2, columnspan=2, padx=10, pady=4, sticky='N')
####################################
delayEntry = ttk.Entry(frameMidOptions, state='disabled', width=7)
delayEntry.grid(row=7, column=0, padx=5, pady=5, columnspan=1, sticky='N')
# Insert frame to display results
frameResults = tk.Frame(root, width=50, height=25)
frameResults.pack_propagate(False)  # Prevents frame from resizing to fit the Treeview
frameResults.grid(row=3, column=0, padx=2, pady=2, sticky="n")
# Set the frame to not expand and fill the space
root.grid_rowconfigure(3, weight=0)  # Adjust the row number as needed
root.grid_columnconfigure(0, weight=0)

frameResults.grid(row=3, column=0, padx=2, pady=2, sticky="n")
root.mainloop()
