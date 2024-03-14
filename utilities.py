# utilities.py
import tkinter as tk
from PIL import Image, ImageTk
import os
from tkinter import filedialog
from tkinter import messagebox

initial_canvas = None

# Function to display initial image on the canvas
def display_initial_image(frame):
    global initial_canvas  # Declare that we're using the global variable
    script_dir = os.path.dirname(os.path.realpath(__file__))
    img_path = os.path.join(script_dir, 'logo/Logo_IA1.png')
    img = ImageTk.PhotoImage(Image.open(img_path))

    if initial_canvas is not None:
        initial_canvas.destroy()  # Destroy the existing canvas if it exists

    #initial_canvas = tk.Canvas(frame, width=340, height=365)
    initial_canvas = tk.Canvas(frame, width=450, height=450)
    initial_canvas.create_image(1, 1, anchor='nw', image=img)
    initial_canvas.grid(row=0, column=0, columnspan=1)
    # Keep a reference to the image to prevent garbage collection
    initial_canvas.image = img

# Function to clear the contents of the frame
def clear_frame(frame):
    global initial_canvas
    if initial_canvas is not None:
        initial_canvas.destroy()  # Destroy the canvas to clear it
    for widget in frame.winfo_children():
        widget.destroy()
