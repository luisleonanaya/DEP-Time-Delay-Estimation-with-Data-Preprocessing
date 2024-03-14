
from tkinter import ttk


def display_lndcf_results_knownDelay(frame, row1, row2, row3, row4):
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
    Display LNDCF results in a Treeview within a specified frame.
    Args:
    frame (tk.Frame): The Tkinter frame where the Treeview will be placed.
    row1 (pd.Series): Data for the first row to be displayed.
    row2 (pd.Series): Data for the second row to be displayed.
    row3 (pd.Series): Data for the third row to be displayed.
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
    # Example of call function
    # display_ccf_results_searchRange(frameResults, row_1_antepenultimate, row_2_penultimate, row_3_last)
