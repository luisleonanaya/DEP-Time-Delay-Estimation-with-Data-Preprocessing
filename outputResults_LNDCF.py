from tkinter import ttk

def display_lndcf_results_knownDelay(frame, row1, row2, row3, row4):
    """
    Displays Locally Normalized Discrete Correlation Function (LNDCF) results for known delays in a
    structured Treeview within a given frame. This function is designed to offer an organized
    visualization of the LNDCF results, emphasizing the statistical details of the analysis.

    Args:
        frame (tk.Frame): The parent frame where the Treeview will be displayed.
        row1 (pd.Series): Series containing data for "Min error" correlation.
        row2 (pd.Series): Series containing data for "Max correlation".
        row3 (pd.Series): Series containing data for "Mean correlation".
        row4 (pd.Series): Series containing data for "Mode correlation".

    This method sets up the Treeview widget with specific columns relevant to LNDCF analysis, such
    as 'LNDCF Max', 'Estimated Delay', among others. It ensures each piece of data is correctly
    placed within its designated column, providing a clear and comprehensive display of the LNDCF
    results for known delays.
    """
    # Create a Treeview widget
    tree_height = 9
    treeDisplay = ttk.Treeview(frame, columns=('Description', 'LNDCF Max', 'Estimated Delay', 'bin', 'delta min', 'delta max', 'uncertainty', 'error'),
                               show="headings", height=tree_height)
    # Define column headings
    treeDisplay.heading("Description", text="Class", anchor='w')
    treeDisplay.heading("LNDCF Max", text="LNDCF max", anchor='center')
    treeDisplay.heading("Estimated Delay", text="delay estimate", anchor='center')
    treeDisplay.heading("bin", text="bin", anchor='center')
    treeDisplay.heading("delta min", text="delta min", anchor='center')
    treeDisplay.heading("delta max", text="delta max", anchor='center')
    treeDisplay.heading("uncertainty", text="uncertainty", anchor='center')
    treeDisplay.heading("error", text="error", anchor='center')
    # Function to insert a row in the Treeview
    def insert_row(description, data_row):
        treeDisplay.insert("", "end", values=(description, f"{data_row['LNDCF_Max']:.5f}",
                                              f"{data_row['EstimatedDelay']:.2f}",
                                              f"{data_row['bin']:.1f}",
                                              f"{data_row['delta min']:.2f}",
                                              f"{data_row['delta max']:.2f}",
                                              f"{data_row['uncertainty']:.1f}",
                                              f"{data_row['error']:.2f}"))
    # Add data to the Treeview
    treeDisplay.insert("", "end", values=("", "", "", "", ""))  # Line break
    insert_row("Min error", row1)
    treeDisplay.insert("", "end", values=("", "", "", "", ""))  # Line break
    insert_row("Max correlation", row2)
    treeDisplay.insert("", "end", values=("", "", "", "", ""))  # Line break
    insert_row("Mean correlation", row3)
    treeDisplay.insert("", "end", values=("", "", "", "", ""))  # Line break
    insert_row("Mode correlation", row4)
    treeDisplay.insert("", "end", values=("", "", "", "", ""))  # Line break
    # Set the minimum width for each column
    treeDisplay.column('Description', anchor='center', minwidth=120, width=130)
    treeDisplay.column('LNDCF Max', anchor='center', minwidth=93, width=102)
    treeDisplay.column('Estimated Delay', anchor='center', minwidth=98, width=108)
    treeDisplay.column('bin', anchor='center', minwidth=40, width=45)
    treeDisplay.column('delta min', anchor='center', minwidth=80, width=85)
    treeDisplay.column('delta max', anchor='center', minwidth=80, width=85)
    treeDisplay.column('uncertainty', anchor='center', minwidth=76, width=80)
    treeDisplay.column('error', anchor='center', minwidth=68, width=73)
    # Set the Treeview in the grid
    treeDisplay.grid(row=0, column=0)
    # display_ccf_results_knownDelay(frameResults, row1_preantepenultimate, row2_antepenultimate, row3_penultimate, row4_last)

def display_lndcf_results_searchRange(frame, row1, row2, row3):
    """
    Showcases LNDCF results for a range of search delays in a concise Treeview format within the
    specified frame. Tailored for cases where the delay is not precisely known but rather searched
    within a defined range, highlighting key statistical outcomes of the LNDCF analysis.

    Args:
        frame (tk.Frame): Frame for embedding the Treeview widget.
        row1 (pd.Series): Series data for "Max correlation" measure.
        row2 (pd.Series): Series data for "Mean correlation" measure.
        row3 (pd.Series): Series data for "Mode correlation" measure.

    The function configures a Treeview widget for visualizing LNDCF results, minus the error column
    used in known delay scenarios, thus focusing on 'LNDCF Max', 'Estimated Delay', and other
    pertinent columns. It aims to deliver a straightforward presentation of the LNDCF findings
    within the context of delay search range analysis.
    """
    # Create a Treeview widget
    tree_height = 7  # Adjusted for three rows
    treeDisplay = ttk.Treeview(frame, columns=('Description', 'LNDCF Max', 'Estimated Delay', 'bin', 'delta min', 'delta max', 'uncertainty'), show="headings", height=tree_height)
    # Define column headings
    treeDisplay.heading("Description", text="Class", anchor='w')
    treeDisplay.heading("LNDCF Max", text="LNDCF max", anchor='center')
    #treeDisplay.heading("LNDCF Err", text="CCF Err", anchor='center')
    treeDisplay.heading("Estimated Delay", text="delay estimate ", anchor='center')
    treeDisplay.heading("bin", text="bin", anchor='center')
    treeDisplay.heading("delta min", text="delta min", anchor='center')
    treeDisplay.heading("delta max", text="delta max", anchor='center')
    treeDisplay.heading("uncertainty", text="uncertainty", anchor='center')
    # Function to insert a row in the Treeview
    def insert_row(description, data_row):
                # Replace NaNs with zero for 'DCF_Err'
        treeDisplay.insert("", "end", values=(description, f"{data_row['LNDCF_Max']:.5f}",
                                              f"{data_row['Estimated Delay']:.2f}",
                                              f"{data_row['bin']:.1f}",
                                              f"{data_row['delta min']:.1f}",
                                              f"{data_row['delta max']:.1f}",
                                              f"{data_row['uncertainty']:.1f}"))
    # Add data to the Treeview
    treeDisplay.insert("", "end", values=("", "", "", "", ""))  # Line break
    insert_row("Max correlation", row1)
    treeDisplay.insert("", "end", values=("", "", "", "", ""))  # Line break
    insert_row("Mean correlation", row2)
    treeDisplay.insert("", "end", values=("", "", "", "", ""))  # Line break
    insert_row("Mode correlation", row3)
    treeDisplay.insert("", "end", values=("", "", "", "", ""))  # Line break
    # Set the minimum width for each column
    treeDisplay.column('Description', anchor='center', minwidth=120, width=130)
    treeDisplay.column('LNDCF Max', anchor='center', minwidth=93, width=102)
    #treeDisplay.column('LNDCF Err', anchor='center', minwidth=93, width=102)
    treeDisplay.column('Estimated Delay', anchor='center', minwidth=98, width=108)
    treeDisplay.column('bin', anchor='center', minwidth=40, width=45)
    treeDisplay.column('delta min', anchor='center', minwidth=80, width=85)
    treeDisplay.column('delta max', anchor='center', minwidth=80, width=85)
    treeDisplay.column('uncertainty', anchor='center', minwidth=76, width=80)
    # Set the Treeview in the grid
    treeDisplay.grid(row=0, column=0)

