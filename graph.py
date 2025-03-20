import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# Initialize lists to store multiple readings
x_readings = []
y_readings = []

def validate_input(values_str):
    try:
        values = list(map(float, values_str.split()))
        return values
    except ValueError:
        messagebox.showerror("Invalid input", "Please enter numbers separated by spaces.")
        return None

def add_reading():
    global x_readings, y_readings

    # Get the values from the input fields
    x_input = wavelength_entry.get()
    y_input = frequency_entry.get()

    x_values = validate_input(x_input)
    y_values = validate_input(y_input)

    if x_values is None or y_values is None:
        return

    if len(x_values) != len(y_values):
        messagebox.showerror("Input Error", "The number of wavelength and frequency values should be the same.")
        return

    # Add the readings to the lists
    x_readings.append(x_values)
    y_readings.append(y_values)

    # Display the input values in the label
    input_values_label.config(text=f"Added Frequencies: {y_input}\nAdded Wavelengths: {x_input}")

def plot_graph():
    global canvas  # Declare canvas as global to modify it

    if not x_readings or not y_readings:
        messagebox.showerror("No Data", "No readings to plot. Please add readings first.")
        return

    # Create a figure and plot the graph
    fig, ax = plt.subplots(figsize=(7, 5))

    for x_values, y_values in zip(x_readings, y_readings):
        ax.plot(y_values, x_values, marker='o', linestyle='-', label=f'Reading {x_readings.index(x_values) + 1}')

    ax.set_xlabel('Frequency (Hz)')
    ax.set_ylabel('Wavelength (nm)')
    ax.set_title('Frequency vs Wavelength Graph')
    ax.grid(True)
    ax.legend()

    # Clear the previous canvas if it exists
    if canvas:
        canvas.get_tk_widget().pack_forget()
        canvas.get_tk_widget().destroy()

    # Embed the figure in Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack()

def calculate_slope():
    if not x_readings or not y_readings:
        messagebox.showerror("No Data", "No readings to calculate slope. Please add readings first.")
        return

    slopes = []
    for x_values, y_values in zip(x_readings, y_readings):
        if len(x_values) < 2 or len(y_values) < 2:
            messagebox.showerror("Insufficient Data", "At least two points are required to calculate the slope.")
            return
        slope, _ = np.polyfit(y_values, x_values, 1)
        slopes.append(slope)

    slope_label.config(text=f"Calculated Slopes: {', '.join(map(str, slopes))}")

# Create the main window
window = tk.Tk()
window.title("Wavelength and Frequency Plotter")
window.configure(background='magenta')
# Create input fields and labels
wavelength_label = tk.Label(window, text="Enter wavelength of light (in nm) separated by spaces:", bg='magenta', fg='white')
wavelength_label.pack()

wavelength_entry = tk.Entry(window, width=40, bg='white', fg='black')
wavelength_entry.pack()

frequency_label = tk.Label(window, text="Enter frequency of light (in Hz) separated by spaces:", bg='magenta', fg='white')
frequency_label.pack()

frequency_entry = tk.Entry(window, width=40, bg='white', fg='black')
frequency_entry.pack()

# Button to add readings
add_button = tk.Button(window, text="Add Reading", command=add_reading, bg='blue', fg='white')
add_button.pack()

# Button to plot the graph
plot_button = tk.Button(window, text="Plot Graph", command=plot_graph, bg='green', fg='white')
plot_button.pack()

# Button to calculate the slope
slope_button = tk.Button(window, text="Calculate Slope", command=calculate_slope, bg='red', fg='white')
slope_button.pack()

# Label to show the input values
input_values_label = tk.Label(window, text="", justify=tk.LEFT, bg='magenta', fg='white')
input_values_label.pack()

# Label to show the calculated slope
slope_label = tk.Label(window, text="", justify=tk.LEFT, bg='magenta', fg='white')
slope_label.pack()

# Initialize the canvas variable
canvas = None

# Start the Tkinter event loop
window.mainloop()
