# utilities.py
import tkinter as tk
from PIL import Image, ImageTk
import os
from tkinter import filedialog
from tkinter import messagebox

initial_canvas = None # Global variable to hold the canvas displaying the initial image

# Function to display initial image on the canvas
def display_initial_image(frame):
    """
    Displays an initial image (e.g., a logo) on a Tkinter canvas within a given frame. This function is typically used to initialize a GUI with a placeholder or branding image.

    Args:
        frame (tk.Frame): The Tkinter frame object where the image will be displayed.

    Returns:
        None: This function does not return a value. Its primary purpose is to display an image on the GUI.

    Raises:
        IOError: If the image file does not exist or cannot be opened, an IOError will be raised.

    Usage:
        This function should be called with a Tkinter frame object as its argument. It creates a new canvas within the frame, loads an image from a predefined path, and displays the image on the canvas. This operation is useful for setting up a branded or initial interface layout.
    """
   
    global initial_canvas  # Use the global canvas variable
    script_dir = os.path.dirname(os.path.realpath(__file__))  # Get the directory of the current script
    img_path = os.path.join(script_dir, 'logo/Logo_IA1.png')  # Construct path to the image
    img = ImageTk.PhotoImage(Image.open(img_path))  # Load the image with PIL
    
    if initial_canvas is not None:
        initial_canvas.destroy()  # If a canvas already exists, destroy it before creating a new one

    initial_canvas = tk.Canvas(frame, width=450, height=450)  # Create a new canvas in the provided frame
    initial_canvas.create_image(1, 1, anchor='nw', image=img)  # Display the image on the canvas
    initial_canvas.grid(row=0, column=0, columnspan=1)  # Position the canvas within the frame
    initial_canvas.image = img  # Keep a reference to the image to prevent it from being garbage-collected

# Function to clear the contents of the frame
def clear_frame(frame):
    """
    Clears all widgets, including a globally referenced canvas, from a given Tkinter frame. This function facilitates dynamic updates to the GUI by removing old widgets before adding new ones.

    Args:
        frame (tk.Frame): The Tkinter frame object from which all child widgets will be removed.

    Returns:
        None: This function does not return a value. It is used to clear widgets from a specified frame.

    Raises:
        None: No explicit errors are raised by this function. It handles the frame's content removal process gracefully.

    Usage:
        This function should be called with a Tkinter frame object as its argument. It checks for a global canvas and destroys it if present, then iteratively destroys all child widgets of the frame. This is essential in GUI applications requiring frequent updates or changes to the displayed content.
    """
    
    global initial_canvas
    if initial_canvas is not None:
        initial_canvas.destroy()# If a global canvas exists, destroy it to clear the space
    for widget in frame.winfo_children():
        widget.destroy() # Destroy each child widget of the frame to clear it
