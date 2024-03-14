from tkinter import filedialog
from tkinter import messagebox

# To optionally save the results csv file
def save_dataframe_to_csv(df_to_save, default_name):
    if df_to_save is not None:
        file_path = filedialog.asksaveasfilename(
            defaultextension='.csv',
            filetypes=[("CSV files", '*.csv'), ("All files", '*.*')],
            title="Save file as...",
            initialfile=default_name
        )
        if file_path:
            try:
                df_to_save.to_csv(file_path, index=True, header=True)
                messagebox.showinfo("Success", f"File saved successfully at {file_path}")
            except Exception as e:
                messagebox.showerror("Save Failed", f"Failed to save file: {e}")
    else:
        messagebox.showerror("Save Failed", "There is no data to save.")

# This is the function that gets called when the save button is pressed.
# It determines which DataFrame to save based on a series of conditions.
def determine_and_save_csv(global_vars):
        # Access global variables via global_vars dictionary
    preprocessing_selectionAA = global_vars['preprocessing_selectionAA']
    delayMethod_selectionAA = global_vars['delayMethod_selectionAA']
    banderaKnownDelay = global_vars['banderaKnownDelay']
    banderaSearchRange = global_vars['banderaSearchRange']
    filteredRawData = global_vars['filteredRawData']
    filteredDiffData = global_vars['filteredDiffData']
    DSv1RawData_SearchRange = global_vars['DSv1RawData_SearchRange']
    DSv1DiffData_SearchRange = global_vars['DSv1DiffData_SearchRange']
    filteredSNR_Data = global_vars['filteredSNR_Data']
    DSv1SNR_Data_SearchRange = global_vars['DSv1SNR_Data_SearchRange']
    filteredWD_Data = global_vars['filteredWD_Data']
    DSv1WD_Data_SearchRange = global_vars['DSv1WD_Data_SearchRange']
    filteredWD2_Data = global_vars['filteredWD2_Data']
    DSv1WD2_Data_SearchRange = global_vars['DSv1WD2_Data_SearchRange']
    filteredWD3_Data = global_vars['filteredWD3_Data']
    DSv1WD3_Data_SearchRange = global_vars['DSv1WD3_Data_SearchRange']
    filteredWD3_Data = global_vars['filteredWD3_Data']
    DSv1WD3_Data_SearchRange = global_vars['DSv1WD3_Data_SearchRange']
    filteredCycle = global_vars['filteredCycle']
    filteredTrend = global_vars['filteredTrend']
    combined_df_CF_KD = global_vars['combined_df_CF_KD']
    combined_df_CF_SR = global_vars['combined_df_CF_SR']
    LNDCF_RawData_KD = global_vars['LNDCF_RawData_KD']
    LNDCF_RawData_SR = global_vars['LNDCF_RawData_SR']
    LNDCF_DiffData = global_vars['LNDCF_DiffData']
    LNDCF_DiffData_SR = global_vars['LNDCF_DiffData_SR']
    LNDCF_SNR_Data = global_vars['LNDCF_SNR_Data']
    LNDCF_SNR_Data_SR = global_vars['LNDCF_SNR_Data_SR']
    LNDCF_CFcycle_Data = global_vars['LNDCF_CFcycle_Data']
    LNDCF_CFtrend_Data = global_vars['LNDCF_CFtrend_Data']
    combined_df_LNDCF_CF_KD = global_vars['combined_df_LNDCF_CF_KD']
    combined_df_LNDCF_CF_SR = global_vars['combined_df_LNDCF_CF_SR']
    LNDCF_WD1_SR = global_vars['LNDCF_WD1_SR']
    LNDCF_WD1_KD = global_vars['LNDCF_WD1_KD']
    LNDCF_WD2_SR = global_vars['LNDCF_WD2_SR']
    LNDCF_WD2_KD = global_vars['LNDCF_WD2_KD']
    LNDCF_WD3_SR = global_vars['LNDCF_WD3_SR']
    LNDCF_WD3_KD = global_vars['LNDCF_WD3_KD']
    DCF_RawData = global_vars['DCF_RawData']
    DCF_RawData_SR = global_vars['DCF_RawData_SR']
    DCF_DiffData = global_vars['DCF_DiffData']
    DCF_DiffData_SR = global_vars['DCF_DiffData_SR']
    DCF_SNR_Data = global_vars['DCF_SNR_Data']
    DCF_SNR_Data_SR = global_vars['DCF_SNR_Data_SR']
    DCF_CFcycle_Data = global_vars['DCF_CFcycle_Data']
    DCF_CFtrend_Data = global_vars['DCF_CFtrend_Data']
    combined_df_DCF_SR = global_vars['combined_df_DCF_SR']
    combined_df_DFC_KD = global_vars['combined_df_DFC_KD']
    DCF_WD1_KD = global_vars['DCF_WD1_KD']
    DCF_WD1_SR = global_vars['DCF_WD1_SR']
    DCF_WD2_KD = global_vars['DCF_WD2_KD']
    DCF_WD2_SR = global_vars['DCF_WD2_SR']
    DCF_WD3_KD = global_vars['DCF_WD3_KD']
    DCF_WD3_SR = global_vars['DCF_WD3_SR']

    if preprocessing_selectionAA == "Raw Data" and delayMethod_selectionAA == "Dispersion Spectra":
        if global_vars['banderaKnownDelay'] == 1:
            if global_vars['filteredRawData'] is not None:
                save_dataframe_to_csv(global_vars['filteredRawData'], "resultsDSv1_RawData_KnownDelay.csv")
            else:
                messagebox.showerror("Save Failed", "The required data for 'Raw Data' with 'Dispersion Spectra' is not available.")
        elif global_vars['banderaSearchRange'] == 1:
            if global_vars['filteredRawData'] is not None:
                save_dataframe_to_csv(global_vars['DSv1RawData_SearchRange'], "resultsDSv1_RawData_SearchRange.csv")
            else:
                messagebox.showerror("Save Failed", "The required data for 'Raw Data' with 'Dispersion Spectra' is not available.")
    #  differenced data with DS
    elif global_vars['preprocessing_selectionAA'] == "Data Differencing" and global_vars['delayMethod_selectionAA'] == "Dispersion Spectra":
        if global_vars['banderaKnownDelay'] == 1:
            if global_vars['filteredDiffData'] is not None:
                save_dataframe_to_csv(global_vars['filteredDiffData'], "resultsDSv1_Differencing_KnownDelay.csv")
            else:
                messagebox.showerror("Save Failed", "The required data for 'Data Differencing' with 'Dispersion Spectra' is not available.")
        elif global_vars['banderaSearchRange'] == 1:
            if global_vars['filteredDiffData'] is not None:
                save_dataframe_to_csv(global_vars['DSv1DiffData_SearchRange'], "resultsDSv1_Differencing_SearchRange.csv")
            else:
                messagebox.showerror("Save Failed", "The required data for 'Data Differencing' with 'Dispersion Spectra' is not available.")
    # Dispersion Spectra with Simple Net Return
    elif global_vars['preprocessing_selectionAA'] == "Simple Net Return" and global_vars['delayMethod_selectionAA'] == "Dispersion Spectra":
        if global_vars['banderaKnownDelay'] == 1:
            if global_vars['filteredSNR_Data'] is not None:
                save_dataframe_to_csv(global_vars['filteredSNR_Data'], "resultsDSv1_SimpleNetReturn_KnownDelay.csv")
            else:
                messagebox.showerror("Save Failed", "The required data for 'Simple Net Return' with 'Dispersion Spectra' is not available.")
        elif global_vars['banderaSearchRange'] == 1:
            if global_vars['filteredSNR_Data'] is not None:
                save_dataframe_to_csv(global_vars['DSv1SNR_Data_SearchRange'], "resultsDSv1_SimpleNetReturn_SearchRange.csv")
            else:
                messagebox.showerror("Save Failed", "The required data for 'Simple Net Return' with 'Dispersion Spectra' is not available.")
    # Dispersion Spectra with Wavelet Denoise lvl 1
    elif global_vars['preprocessing_selectionAA'] == "Wavelet Denoise lvl 1" and global_vars['delayMethod_selectionAA'] == "Dispersion Spectra":
        if global_vars['banderaKnownDelay'] == 1:
            if global_vars['filteredWD_Data'] is not None:
                save_dataframe_to_csv(global_vars['filteredWD_Data'], "resultsDSv1_WDlvl1_KnownDelay.csv")
            else:
                messagebox.showerror("Save Failed", "The required data for 'Wavelet Denoise lvl 1' with 'Dispersion Spectra' is not available.")
        elif global_vars['banderaSearchRange'] == 1:
            if global_vars['filteredWD_Data'] is not None:
                save_dataframe_to_csv(global_vars['DSv1WD_Data_SearchRange'], "resultsDSv1_WDlvl1_SearchRange.csv")
            else:
                messagebox.showerror("Save Failed", "The required data for 'Wavelet Denoise lvl 1' with 'Dispersion Spectra' is not available.")
    # Dispersion Spectra with Wavelet Denoise lvl 2
    elif global_vars['preprocessing_selectionAA'] == "Wavelet Denoise lvl 2" and global_vars['delayMethod_selectionAA']  == "Dispersion Spectra":
        if global_vars['banderaKnownDelay'] == 1:
            if global_vars['filteredWD2_Data']  is not None:
                save_dataframe_to_csv(global_vars['filteredWD2_Data'], "resultsDSv1_WDlvl2_KnownDelay.csv")
            else:
                messagebox.showerror("Save Failed", "The required data for 'Wavelet Denoise lvl 2' with 'Dispersion Spectra' is not available.")
        elif global_vars['banderaSearchRange'] == 1:
            if global_vars['filteredWD2_Data'] is not None:
                save_dataframe_to_csv(global_vars['DSv1WD2_Data_SearchRange'], "resultsDSv1_WDlvl2_SearchRange.csv")
            else:
                messagebox.showerror("Save Failed", "The required data for 'Wavelet Denoise lvl 2' with 'Dispersion Spectra' is not available.")
    # Dispersion Spectra with Wavelet Denoise lvl 3
    elif global_vars['preprocessing_selectionAA'] == "Wavelet Denoise lvl 3" and global_vars['delayMethod_selectionAA']  == "Dispersion Spectra":
        if global_vars['banderaKnownDelay'] == 1:
            if global_vars['filteredWD3_Data'] is not None:
                save_dataframe_to_csv(global_vars['filteredWD3_Data'], "resultsDSv1_WDlvl3_KnownDelay.csv")
            else:
                messagebox.showerror("Save Failed", "The required data for 'Wavelet Denoise lvl 2' with 'Dispersion Spectra' is not available.")
        elif global_vars['banderaSearchRange'] == 1:
            if global_vars['filteredWD3_Data'] is not None:
                save_dataframe_to_csv(global_vars['DSv1WD3_Data_SearchRange'], "resultsDSv1_WDlvl3_SearchRange.csv")
            else:
                messagebox.showerror("Save Failed", "The required data for 'Wavelet Denoise lvl 2' with 'Dispersion Spectra' is not available.")
    # Dispersion Spectra with  Christiano-Fitzgerald filter
    elif global_vars['preprocessing_selectionAA'] == "Christiano-Fitzgerald filter" and global_vars['delayMethod_selectionAA']  == "Dispersion Spectra":
        if global_vars['banderaKnownDelay'] == 1:
            if global_vars['filteredCycle'] is not None and global_vars['filteredTrend'] is not None:
                save_dataframe_to_csv(global_vars['combined_df_CF_KD'], "resultsDSv1_CF_cycle_trend_KnownDelay.csv")
            else:
                messagebox.showerror("Save Failed", "The required data for 'Christiano-Fitzgerald filter' with 'Dispersion Spectra' is not available.")
        elif banderaSearchRange == 1:
            if global_vars['filteredCycle'] is not None and global_vars['filteredTrend'] is not None:
                save_dataframe_to_csv(global_vars['combined_df_CF_SR'], "resultsDSv1_CF_cycle_trend_SearchRange.csv")
            else:
                messagebox.showerror("Save Failed", "The required data for 'Christiano-Fitzgerald filter' with 'Dispersion Spectra' is not available.")
    # Locally Normalized DCF with raw data
    elif global_vars['preprocessing_selectionAA'] == "Raw Data" and global_vars['delayMethod_selectionAA'] == "Locally Normalized DCF":
        if global_vars['banderaKnownDelay'] == 1:
            if global_vars['LNDCF_RawData_KD'] is not None:
                save_dataframe_to_csv(global_vars['LNDCF_RawData_KD'], "resultsLNDCF_RawData_KnownDelay.csv")
            else:
                messagebox.showerror("Save Failed", "The required data for 'Raw Data' with 'Locally Normalized DCF' is not available.")
        elif global_vars['banderaSearchRange'] == 1:
            if global_vars['LNDCF_RawData_SR'] is not None:
                save_dataframe_to_csv(global_vars['LNDCF_RawData_SR'], "resultsLNDCF_RawData_SearchRange.csv")

            else:
                messagebox.showerror("Save Failed", "The required data for 'Raw Data' with 'Locally Normalized DCF' is not available.")
    # Locally Normalized DCF with data differencing
    elif global_vars['preprocessing_selectionAA'] == "Data Differencing" and global_vars['delayMethod_selectionAA'] == "Locally Normalized DCF":
        if global_vars['banderaKnownDelay'] == 1:
            if global_vars['LNDCF_DiffData'] is not None:
                save_dataframe_to_csv(global_vars['LNDCF_DiffData'], "resultsLNDCF_DiffData_KnownDelay.csv")
            else:
                messagebox.showerror("Save Failed", "The required data for 'Data Differencing' with 'Locally Normalized DCF' is not available.")
        elif global_vars['banderaSearchRange'] == 1:
            if global_vars['LNDCF_DiffData_SR'] is not None:
                save_dataframe_to_csv(global_vars['LNDCF_DiffData_SR'], "resultsLNDCF_DiffData_SearchRange.csv")
            else:
                messagebox.showerror("Save Failed", "The required data for 'Data Differencing' with 'Locally Normalized DCF' is not available.")
    # Locally Normalized DCF with Simple Net Return
    elif global_vars['preprocessing_selectionAA'] == "Simple Net Return" and global_vars['delayMethod_selectionAA'] == "Locally Normalized DCF":
        if global_vars['banderaKnownDelay'] == 1:
            if global_vars['LNDCF_SNR_Data'] is not None:
                save_dataframe_to_csv(global_vars['LNDCF_SNR_Data'], "resultsLNDCF_SimpleNetReturn_KnownDelay.csv")
            else:
                messagebox.showerror("Save Failed", "The required data for 'Simple Net Return' with 'Locally Normalized DCF' is not available.")
        elif global_vars['banderaSearchRange'] == 1:
            if global_vars['LNDCF_SNR_Data_SR'] is not None:
                save_dataframe_to_csv(global_vars['LNDCF_SNR_Data_SR'], "resultsLNDCF_SimpleNetReturn_SearchRange.csv")
            else:
                messagebox.showerror("Save Failed", "The required data for 'Simple Net Return' with 'Locally Normalized DCF' is not available.")
    # Locally Normalized DCF with Christiano-Fitzgerald filter
    elif global_vars['preprocessing_selectionAA'] == "Christiano-Fitzgerald filter" and global_vars['delayMethod_selectionAA'] == "Locally Normalized DCF":
        if global_vars['banderaKnownDelay'] == 1:
            if global_vars['LNDCF_CFcycle_Data'] is not None and global_vars['LNDCF_CFtrend_Data'] is not None:
                save_dataframe_to_csv(global_vars['combined_df_LNDCF_CF_KD'], "resultsLNDCF_CF_cycle_trend_KnownDelay.csv")
            else:
                messagebox.showerror("Save Failed", "The required data for 'Christiano-Fitzgerald filter' with 'Locally Normalized DCF' is not available.")
        elif global_vars['banderaSearchRange'] == 1:
            if global_vars['LNDCF_CFcycle_Data'] is not None and global_vars['LNDCF_CFtrend_Data'] is not None:
                save_dataframe_to_csv(global_vars['combined_df_LNDCF_CF_SR'], "resultsLNDCF_CF_cycle_trend_SearchRange.csv")
            else:
                messagebox.showerror("Save Failed", "The required data for 'Christiano-Fitzgerald filter' with 'Locally Normalized DCF' is not available.")
    # Locally Normalized DCF with Wavelet denoising level 1
    elif global_vars['preprocessing_selectionAA'] == "Wavelet Denoise lvl 1" and global_vars['delayMethod_selectionAA'] == "Locally Normalized DCF":
        if global_vars['banderaKnownDelay'] == 1:
            if global_vars['LNDCF_WD1_KD'] is not None:
                save_dataframe_to_csv(LNDCF_WD1_KD, "resultsLNDCF_WDlvl1_KnownDelay.csv")
            else:
                messagebox.showerror("Save Failed", "The required data for 'Wavelet Denoise lvl 1' with 'Locally Normalized DCF' is not available.")
        elif global_vars['banderaSearchRange'] == 1:
            if global_vars['LNDCF_WD1_SR'] is not None:
                save_dataframe_to_csv(LNDCF_WD1_SR, "resultsLNDCF_WDlvl1_SearchRange.csv")
            else:
                messagebox.showerror("Save Failed", "The required data for 'Wavelet Denoise lvl 1' with 'Locally Normalized DCF' is not available.")
    # Locally Normalized DCF with Wavelet denoising level 2
    elif global_vars['preprocessing_selectionAA'] == "Wavelet Denoise lvl 2" and delayMethod_selectionAA == "Locally Normalized DCF":
        if global_vars['banderaKnownDelay'] == 1:
            if global_vars['LNDCF_WD2_KD'] is not None:
                save_dataframe_to_csv(LNDCF_WD2_KD, "resultsLNDCF_WDlvl2_KnownDelay.csv")
            else:
                messagebox.showerror("Save Failed", "The required data for 'Wavelet Denoise lvl 2' with 'Locally Normalized DCF' is not available.")
        elif global_vars['banderaSearchRange'] == 1:
            if global_vars['LNDCF_WD2_SR'] is not None:
                save_dataframe_to_csv(LNDCF_WD2_SR, "resultsLNDCF_WDlvl2_SearchRange.csv")
            else:
                messagebox.showerror("Save Failed", "The required data for 'Wavelet Denoise lvl 2' with 'Locally Normalized DCF' is not available.")
    # Locally Normalized DCF with Wavelet denoising level 3
    elif global_vars['preprocessing_selectionAA'] == "Wavelet Denoise lvl 3" and global_vars['delayMethod_selectionAA'] == "Locally Normalized DCF":
        if global_vars['banderaKnownDelay'] == 1:
            if global_vars['LNDCF_WD3_KD'] is not None:
                save_dataframe_to_csv(LNDCF_WD3_KD, "resultsLNDCF_WDlvl3_KnownDelay.csv")
            else:
                messagebox.showerror("Save Failed", "The required data for 'Wavelet Denoise lvl 3' with 'Locally Normalized DCF' is not available.")
        elif global_vars['banderaSearchRange'] == 1:
            if global_vars['LNDCF_WD3_SR'] is not None:
                save_dataframe_to_csv(LNDCF_WD3_SR, "resultsLNDCF_WDlvl3_SearchRange.csv")
            else:
                messagebox.showerror("Save Failed", "The required data for 'Wavelet Denoise lvl 3' with 'Locally Normalized DCF' is not available.")
    # Discrete Correlation Function (DCF) with raw data
    elif global_vars['preprocessing_selectionAA'] == "Raw Data" and global_vars['delayMethod_selectionAA'] == "Discrete Correlation Function (DCF)":
        if global_vars['banderaKnownDelay'] == 1:
            if global_vars['DCF_RawData'] is not None:
                save_dataframe_to_csv(global_vars['DCF_RawData'], "resultsDCF_RawData_KnownDelay.csv")
            else:
                messagebox.showerror("Save Failed", "The required data for 'Raw Data' with 'Discrete Correlation Function (DCF)' is not available.")
        elif global_vars['banderaSearchRange'] == 1:
            if global_vars['DCF_RawData'] is not None:
                save_dataframe_to_csv(global_vars['DCF_RawData_SR'], "resultsDCF_RawData_SearchRange.csv")
            else:
                messagebox.showerror("Save Failed", "The required data for 'Raw Data' with 'Discrete Correlation Function (DCF)' is not available.")
    # Discrete Correlation Function (DCF) with Data Differencing
    elif global_vars['preprocessing_selectionAA'] == "Data Differencing" and global_vars['delayMethod_selectionAA'] == "Discrete Correlation Function (DCF)":
        if global_vars['banderaKnownDelay'] == 1:
            if global_vars['DCF_DiffData'] is not None:
                save_dataframe_to_csv(global_vars['DCF_DiffData'], "resultsDCF_Differencing_KnownDelay.csv")
            else:
                messagebox.showerror("Save Failed", "The required data for 'Data Differencing' with 'Discrete Correlation Function (DCF)' is not available.")
        elif global_vars['banderaSearchRange'] == 1:
            if DCF_DiffData_SR is not None:
                save_dataframe_to_csv(DCF_DiffData_SR, "resultsDCF_Differencing_SearchRange.csv")
            else:
                messagebox.showerror("Save Failed", "The required data for 'Data Differencing' with 'Discrete Correlation Function (DCF)' is not available.")
    # Discrete Correlation Function (DCF) with Simple Net Return
    elif global_vars['preprocessing_selectionAA'] == "Simple Net Return" and global_vars['delayMethod_selectionAA'] == "Discrete Correlation Function (DCF)":
        if global_vars['banderaKnownDelay'] == 1:
            if global_vars['DCF_SNR_Data'] is not None:
                save_dataframe_to_csv(global_vars['DCF_SNR_Data'], "resultsDCF_SimpleNetReturn_KnownDelay.csv")
            else:
                messagebox.showerror("Save Failed", "The required data for 'Simple Net Return' with 'Discrete Correlation Function (DCF)' is not available.")
        elif global_vars['banderaSearchRange'] == 1:
            if global_vars['DCF_SNR_Data_SR'] is not None:
                save_dataframe_to_csv(global_vars['DCF_SNR_Data_SR'], "resultsDCF_SimpleNetReturn_SearchRange.csv")
            else:
                messagebox.showerror("Save Failed", "The required data for 'Simple Net Return' with 'Discrete Correlation Function (DCF)' is not available.")
    # Discrete Correlation Function (DCF) with Christiano-Fitzgerald filter
    elif global_vars['preprocessing_selectionAA'] == "Christiano-Fitzgerald filter" and global_vars['delayMethod_selectionAA'] == "Discrete Correlation Function (DCF)":
        if global_vars['banderaKnownDelay'] == 1:
            if global_vars['DCF_CFcycle_Data'] is not None and global_vars['DCF_CFtrend_Data'] is not None:
                save_dataframe_to_csv(global_vars['combined_df_DFC_KD'], "resultsDCF_CF_cycle_trend_KnownDelay.csv")
            else:
                messagebox.showerror("Save Failed", "The required data for 'Christiano-Fitzgerald filter' with 'Discrete Correlation Function (DCF)' is not available.")
        elif global_vars['banderaSearchRange'] == 1:
            if global_vars['DCF_CFcycle_Data'] is not None and global_vars['DCF_CFtrend_Data'] is not None:
                save_dataframe_to_csv(global_vars['combined_df_DCF_SR'], "resultsDCF_CF_cycle_trend_SearchRange.csv")
            else:
                messagebox.showerror("Save Failed", "The required data for 'Christiano-Fitzgerald filter' with 'Discrete Correlation Function (DCF)' is not available.")
    # Discrete Correlation Function (DCF) with Wavelet Denoise lvl 1
    elif global_vars['preprocessing_selectionAA'] == "Wavelet Denoise lvl 1" and global_vars['delayMethod_selectionAA'] == "Discrete Correlation Function (DCF)":
        if global_vars['banderaKnownDelay'] == 1:
            if global_vars['DCF_WD1_KD'] is not None:
                save_dataframe_to_csv(global_vars['DCF_WD1_KD'], "resultsDCF_WDlvl1_KnownDelay.csv")
            else:
                messagebox.showerror("Save Failed", "The required data for 'Wavelet Denoise lvl 1' with 'Discrete Correlation Function (DCF)' is not available.")
        elif global_vars['banderaSearchRange'] == 1:
            if global_vars['DCF_WD1_SR'] is not None:
                save_dataframe_to_csv(global_vars['DCF_WD1_SR'], "resultsDCF_WDlvl1_SearchRange.csv")
            else:
                messagebox.showerror("Save Failed", "The required data for 'Wavelet Denoise lvl 1' with 'Discrete Correlation Function (DCF)' is not available.")
    # Discrete Correlation Function (DCF) with Wavelet Denoise lvl 2
    elif global_vars['preprocessing_selectionAA'] == "Wavelet Denoise lvl 2" and global_vars['delayMethod_selectionAA'] == "Discrete Correlation Function (DCF)":
        if global_vars['banderaKnownDelay'] == 1:
            if global_vars['DCF_WD2_KD'] is not None:
                save_dataframe_to_csv(global_vars['DCF_WD2_KD'], "resultsDCF_WDlvl2_KnownDelay.csv")
            else:
                messagebox.showerror("Save Failed", "The required data for 'Wavelet Denoise lvl 2' with 'Discrete Correlation Function (DCF)' is not available.")
        elif global_vars['banderaSearchRange'] == 1:
            if global_vars['DCF_WD2_SR'] is not None:
                save_dataframe_to_csv(global_vars['DCF_WD2_SR'], "resultsDCF_WDlvl2_SearchRange.csv")
            else:
                messagebox.showerror("Save Failed", "The required data for 'Wavelet Denoise lvl 2' with 'Discrete Correlation Function (DCF)' is not available.")
    # Discrete Correlation Function (DCF) with Wavelet Denoise lvl 3
    elif global_vars['preprocessing_selectionAA'] == "Wavelet Denoise lvl 3" and global_vars['delayMethod_selectionAA'] == "Discrete Correlation Function (DCF)":
        if global_vars['banderaKnownDelay'] == 1:
            if global_vars['DCF_WD3_KD'] is not None:
                save_dataframe_to_csv(global_vars['DCF_WD3_KD'], "resultsDCF_WDlvl3_KnownDelay.csv")
            else:
                messagebox.showerror("Save Failed", "The required data for 'Wavelet Denoise lvl 3' with 'Discrete Correlation Function (DCF)' is not available.")
        elif global_vars['banderaSearchRange'] == 1:
            if global_vars['DCF_WD3_SR'] is not None:
                save_dataframe_to_csv(global_vars['DCF_WD3_SR'], "resultsDCF_WDlvl3_SearchRange.csv")
            else:
                messagebox.showerror("Save Failed", "The required data for 'Wavelet Denoise lvl 3' with 'Discrete Correlation Function (DCF)' is not available.")
    return global_vars
