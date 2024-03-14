import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import filedialog


def display_DSV1_results_knownDelay(frame, row1, row2, row3, row4):
    # Create a Treeview widget
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
        # Create a Treeview widget
    tree_height = 7
    treeDisplay = ttk.Treeview(frame, columns=('Class', 'Estimated Delay', 'delta min', 'delta max', 'uncertainty', '---'),
                               show="headings", height=tree_height)
    # Define column headings
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
    # display_results_in_treeview_3rows(frameResults, row_1_antepenultimate, row_2_penultimate, row_3_last)
