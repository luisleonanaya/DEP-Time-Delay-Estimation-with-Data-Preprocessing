import io
import os
from reportlab.platypus import SimpleDocTemplate, Spacer, Image, Paragraph, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.units import inch
from tkinter import Tk, filedialog, messagebox
#import matplotlib.pyplot as plt

additional_figure_width = 6.6  # Width of the additional figure in inches
additional_figure_height = 5.0  # Height of the additional figure in inches
figures_width = [5.8, 5.8]  # Widths of the figures in inches
figures_height = [4.6, 4.6]  # Heights of the figures in inches

# Function to convert a Matplotlib figure to a PIL Image and set its size
def convert_fig_to_image(fig, width, height):
    buf = io.BytesIO()
    fig.savefig(buf, format='PNG')
    buf.seek(0)
    img = Image(buf)
    img.drawWidth = width * inch
    img.drawHeight = height * inch
    return img

# Function to create a PDF with histograms, statistics tables, and additional figures
def export_histogram_and_stats_to_pdf(figures, stats_data, headers, additional_figure, additional_header, initial_dir, initial_file):
    root = Tk()
    root.withdraw()  # Hide the Tkinter root window
    file_path = filedialog.asksaveasfilename(initialdir=initial_dir, initialfile=initial_file, filetypes=[("PDF files", "*.pdf")])
    root.destroy()  # Destroy the Tkinter window to prevent it from running

    if not file_path:  # Check if the user cancelled the file dialog
        return

    pdf_doc = SimpleDocTemplate(file_path, pagesize=landscape(letter))  # Create the PDF document
    story = []
    styles = getSampleStyleSheet()

    # Add additional figure and header if provided
    if additional_figure and additional_header:
        img = convert_fig_to_image(additional_figure, additional_figure_width, additional_figure_height)
        story.append(Paragraph(additional_header, styles['Title']))
        story.append(img)
        story.append(Spacer(1, 0.9 * inch))

    # Add histogram figures and statistics tables
    for fig, stat, header, fig_width, fig_height in zip(figures, stats_data, headers, figures_width, figures_height):
        img = convert_fig_to_image(fig, fig_width, fig_height)  # Convert the matplotlib figure to an image

        # Split the statistics data into lines and create a table row for each line
        stat_table_data = [[Paragraph(s, styles['Normal'])] for s in stat.split('\n')]
        stat_table = Table(stat_table_data, colWidths=[2 * inch])  # Create a table for the statistics
        stat_table.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 1, colors.black),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ]))

        data = [[img, stat_table]]  # Combine the image and statistics table in a row
        table = Table(data)  # Create a table to hold the combined row
        story.append(Paragraph(header, styles['Title']))
        story.append(table)
        story.append(Spacer(1, 1.1 * inch))

    # Build the PDF with the content from the story list
    pdf_doc.build(story)
    messagebox.showinfo("Success", "The PDF was successfully created.")  # Show a success message

