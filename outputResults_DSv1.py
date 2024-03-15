import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import filedialog


def display_DSV1_results_knownDelay(frame, row1, row2, row3, row4):
    """
    Displays the results of a Dispersion Spectra Version 1 (DSv1) analysis in a structured Treeview
    widget, specifically designed for scenarios where delay information is already known. It
    showcases rows that represent various statistical interpretations of the data.

    Args:
        frame (tk.Frame): The parent Tkinter frame where the Treeview will be embedded.
        row1 (pd.Series): The data series for the row indicating "Min estimated" delay.
        row2 (pd.Series): The data series for the row indicating "Mean estimated" delay.
        row3 (pd.Series): The data series for the row indicating "Mode estimated" delay.
        row4 (pd.Series): The data series for the row indicating "Avg. mean+mode" delay.

    Returns:
        None

    This function constructs a Treeview widget within the specified frame, configuring it with
    columns relevant to DSv1 analysis results, and populates it with provided data series. Each
    column is tailored to display specific aspects of the analysis outcome.
    """
    # Configuration and setup of the Treeview widget for DSv1 results
    tree_height = 9
    treeDisplay = ttk.Treeview(frame, columns=('Class', 'Estimated Delay', 'delta min', 'delta max', 'uncertainty', 'error'),
                               show="headings", height=tree_height)
    # Define column headings
    treeDisplay.heading("Class", text="Class", anchor='w')  # 'w' stands for west (left)
    treeDisplay.heading("Estimated Delay", text="delay estimate", anchor='center')
    treeDisplay.heading("delta min", text="delta min", anchor='center')
    treeDisplay.heading("delta max", text="delta max", anchor='center')
    treeDisplay.heading("uncertainty", text="uncertainty", anchor='center')
    treeDisplay.heading("error", text="error", anchor='center')
    # Function to insert a row in the Treeview
    def insert_row(title, data_row):
        treeDisplay.insert("", "end", values=(title, f"{data_row['EstimatedDelay']:.2f}",
                                              f"{data_row['delta_min']:.2f}",
                                              f"{data_row['delta_max']:.2f}",
                                              f"{data_row['uncertainty']:.2f}",
                                              f"{data_row['error']:.2f}"))
    # Add data to the Treeview
    treeDisplay.insert("", "end", values=("", "", "", "", ""))  # Line break
    insert_row("Min estimated", row1)
    treeDisplay.insert("", "end", values=("", "", "", "", ""))  # Line break
    insert_row("Mean estimated", row2)
    treeDisplay.insert("", "end", values=("", "", "", "", ""))  # Line break
    insert_row("Mode estimated", row3)
    treeDisplay.insert("", "end", values=("", "", "", "", ""))  # Line break
    insert_row("Avg. mean+mode", row4)
    treeDisplay.insert("", "end", values=("", "", "", "", ""))  # Line break
    # Set the minimum width for each column
    treeDisplay.column('Class', anchor='center', minwidth=125, width=130)
    treeDisplay.column('Estimated Delay', anchor='center', minwidth=108, width=118)
    treeDisplay.column('delta min', anchor='center', minwidth=95, width=105)
    treeDisplay.column('delta max', anchor='center', minwidth=95, width=105)
    treeDisplay.column('uncertainty', anchor='center', minwidth=80, width=90)
    treeDisplay.column('error', anchor='center', minwidth=85, width=95)
    # Set the Treeview in the grid
    treeDisplay.grid(row=0, column=0)
    # display_results_in_treeview(frameResults, row_one_preantepenultimate, row_two_antepenultimate, row_three_penultimate, row_four_last)

def display_DSV1_results_searchRange(frame, row1, row2, row3):
    """
    Displays DSv1 analysis results in a Treeview widget, tailored for scenarios where a range of delays
    is being searched. It visualizes the data in a concise format that omits the error column and
    highlights certain rows for emphasis.

    Args:
        frame (tk.Frame): The frame in which the Treeview is to be displayed.
        row1 (pd.Series): Data for the first row, typically showing "Mean estimated" delay.
        row2 (pd.Series): Data for the second row, typically showing "Mode estimated" delay.
        row3 (pd.Series): Data for the third row, typically showing "Avg. mean+mode" delay.

    Returns:
        None

    This function is similar to `display_DSV1_results_knownDelay` but adjusted to the context of
    search range scenarios. It omits the 'error' column and utilizes a 'gray_background' tag to
    highlight specific rows, aiding in distinguishing between different statistical measures.
    """
    # Create a Treeview widget
    tree_height = 7
    treeDisplay = ttk.Treeview(frame, columns=('Class', 'Estimated Delay', 'delta min', 'delta max', 'uncertainty', '---'),
                               show="headings", height=tree_height)
    # Define column headings and setup
    # Column titles are set to guide user interpretation of the displayed data
    treeDisplay.heading("Class", text="Class", anchor='w')
    treeDisplay.heading("Estimated Delay", text="delay estimate", anchor='center')
    treeDisplay.heading("delta min", text="delta min", anchor='center')
    treeDisplay.heading("delta max", text="delta max", anchor='center')
    treeDisplay.heading("uncertainty", text="uncertainty", anchor='center')
    treeDisplay.heading("---", text="---", anchor='center')
    # Tag configuration for rows with a gray background
    treeDisplay.tag_configure("gray_background", background="lightgrey")
    # Function to insert a row in the Treeview
    def insert_row(title, data_row, tag=None):
        if tag:
            treeDisplay.insert("", "end", values=(title, f"{data_row['Estimated Delay']:.2f}",
                                                  f"{data_row['delta min']:.2f}",
                                                  f"{data_row['delta max']:.2f}",
                                                  f"{data_row['uncertainty']:.2f}"), tags=(tag,))
        else:
            treeDisplay.insert("", "end", values=(title, f"{data_row['Estimated Delay']:.2f}",
                                                  f"{data_row['delta min']:.2f}",
                                                  f"{data_row['delta max']:.2f}",
                                                  f"{data_row['uncertainty']:.2f}"))
    # Add data to the Treeview
    treeDisplay.insert("", "end", values=("", "", "", "", ""))  # Line break
    insert_row("Mean estimated", row1, "gray_background")
    treeDisplay.insert("", "end", values=("", "", "", "", ""))  # Line break
    insert_row("Mode estimated", row2)
    treeDisplay.insert("", "end", values=("", "", "", "", ""))  # Line break
    insert_row("Avg. mean+mode", row3)
    # Set the minimum width for each column
    treeDisplay.column('Class', anchor='center', minwidth=125, width=130)
    treeDisplay.column('Estimated Delay', anchor='center', minwidth=110, width=120)
    treeDisplay.column('delta min', anchor='center', minwidth=100, width=105)
    treeDisplay.column('delta max', anchor='center', minwidth=100, width=105)
    treeDisplay.column('uncertainty', anchor='center', minwidth=80, width=90)
    treeDisplay.column('---', anchor='center', minwidth=85, width=95)
    # Set the Treeview in the grid
    treeDisplay.grid(row=0, column=0)

