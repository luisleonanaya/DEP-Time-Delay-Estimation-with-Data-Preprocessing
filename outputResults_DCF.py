from tkinter import ttk

def display_dcf_results_knownDelay(frame, row1, row2, row3, row4):
    """
    Displays the results of the Discrete Correlation Function (DCF) analysis in a Treeview widget,
    tailored for scenarios where the delay is known. It includes specific rows representing different
    statistical metrics (Min error, Max correlation, Mean correlation, Mode correlation).

    Args:
        frame (tk.Frame): The frame within which the Treeview will be embedded.
        row1 (pd.Series): The data series for the row labeled "Min error."
        row2 (pd.Series): The data series for the row labeled "Max correlation."
        row3 (pd.Series): The data series for the row labeled "Mean correlation."
        row4 (pd.Series): The data series for the row labeled "Mode correlation."

    Returns:
        None

    This function constructs a Treeview widget with headings relevant to DCF results,
    then populates it with the data provided through the row arguments. It configures column widths
    and sets the widget in the designated frame.
    """
    # Configuration and setup of the Treeview widget for DCF results display
    tree_height = 9  # Display height for four rows
    treeDisplay = ttk.Treeview(frame, columns=('Description', 'DCF Max', 'EstimatedDelay', 'bin', 'delta min', 'delta max', 'uncertainty', 'error'),
                               show="headings", height=tree_height)
    # Define column headings and their text
    # Setting up each column's display properties
    treeDisplay.heading("Description", text="Class", anchor='w')
    treeDisplay.heading("DCF Max", text="DCF max", anchor='center')
    treeDisplay.heading("EstimatedDelay", text="delay estimate", anchor='center')
    treeDisplay.heading("bin", text="bin", anchor='center')
    treeDisplay.heading("delta min", text="delta min", anchor='center')
    treeDisplay.heading("delta max", text="delta max", anchor='center')
    treeDisplay.heading("uncertainty", text="uncertainty", anchor='center')
    treeDisplay.heading("error", text="error", anchor='center')
    # Internal function to insert a single row into the Treeview
    def insert_row(description, data_row):
    # Inserting a row with formatted values
        treeDisplay.insert("", "end", values=(description, f"{data_row['DCF_Max']:.5f}",
                                              f"{data_row['EstimatedDelay']:.2f}",
                                              f"{data_row['bin']:.1f}",
                                              f"{data_row['delta min']:.2f}",
                                              f"{data_row['delta max']:.2f}",
                                              f"{data_row['uncertainty']:.1f}",
                                              f"{data_row['error']:.2f}"))
    # Populating the Treeview with data
    # Empty rows are inserted for visual spacing
    treeDisplay.insert("", "end", values=("", "", "", "", ""))  # Line break
    insert_row("Min error", row1)
    treeDisplay.insert("", "end", values=("", "", "", "", ""))  # Line break
    insert_row("Max correlation", row2)
    treeDisplay.insert("", "end", values=("", "", "", "", ""))  # Line break
    insert_row("Mean correlation", row3)
    treeDisplay.insert("", "end", values=("", "", "", "", ""))  # Line break
    insert_row("Mode correlation", row4)
    treeDisplay.insert("", "end", values=("", "", "", "", ""))  # Line break
    # Column configuration for better layout
    treeDisplay.column('Description', anchor='center', minwidth=120, width=130)
    treeDisplay.column('DCF Max', anchor='center', minwidth=93, width=102)
    treeDisplay.column('EstimatedDelay', anchor='center', minwidth=93, width=102)
    treeDisplay.column('bin', anchor='center', minwidth=40, width=45)
    treeDisplay.column('delta min', anchor='center', minwidth=80, width=85)
    treeDisplay.column('delta max', anchor='center', minwidth=80, width=85)
    treeDisplay.column('uncertainty', anchor='center', minwidth=76, width=80)
    treeDisplay.column('error', anchor='center', minwidth=76, width=80)
    # Set the Treeview in the grid
    treeDisplay.grid(row=0, column=0)
    
    
# Setup for the Treeview is similar to `display_dcf_results_knownDelay`
# This version is tailored for displaying three specific types of result rows for search range scenarios
# The 'insert_row' function is reused for inserting data rows into the Treeview
def display_dcf_results_searchRange(frame, row1, row2, row3):
    """
    Displays DCF analysis results for a search range scenario, presenting data in three specific rows
    within a Treeview widget. This function is optimized for cases where a broader range of delay values is explored.

    Args:
        frame (tk.Frame): The frame to contain the Treeview.
        row1 (pd.Series): Data series for the row labeled "Max correlation."
        row2 (pd.Series): Data series for the row labeled "Mean correlation."
        row3 (pd.Series): Data series for the row labeled "Mode correlation."

    Returns:
        None

    Similar to `display_dcf_results_knownDelay`, this function creates and populates a Treeview widget
    but adjusts for three rows of data and omits the 'DCF_Err' column, focusing on scenarios with variable delay ranges.
    """
    # Create a Treeview widget
    tree_height = 7  # Set to display three rows
    treeDisplay = ttk.Treeview(frame, columns=('Description', 'DCF Max', 'EstimatedDelay', 'bin', 'delta min', 'delta max', 'uncertainty'),
                               show="headings", height=tree_height)
    # Define column headings
    treeDisplay.heading("Description", text="Class", anchor='w')
    treeDisplay.heading("DCF Max", text="DCF max", anchor='center')
    treeDisplay.heading("EstimatedDelay", text="delay estimate", anchor='center')
    treeDisplay.heading("bin", text="bin", anchor='center')
    treeDisplay.heading("delta min", text="delta min", anchor='center')
    treeDisplay.heading("delta max", text="delta max", anchor='center')
    treeDisplay.heading("uncertainty", text="uncertainty", anchor='center')
    # Function to insert a row in the Treeview
    def insert_row(description, data_row):
        treeDisplay.insert("", "end", values=(description, f"{data_row['DCF_Max']:.5f}",
                                              f"{data_row['EstimatedDelay']:.2f}",
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
    treeDisplay.column('DCF Max', anchor='center', minwidth=93, width=102)
    treeDisplay.column('EstimatedDelay', anchor='center', minwidth=93, width=102)
    treeDisplay.column('bin', anchor='center', minwidth=40, width=45)
    treeDisplay.column('delta min', anchor='center', minwidth=80, width=85)
    treeDisplay.column('delta max', anchor='center', minwidth=80, width=85)
    treeDisplay.column('uncertainty', anchor='center', minwidth=76, width=80)
    # Set the Treeview in the grid
    treeDisplay.grid(row=0, column=0)

