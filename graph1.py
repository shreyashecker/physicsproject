import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# Initialize lists to store multiple readings
x_readings = []  # Wavelength (λ) in meters
y_readings = []  # 1/Frequency (1/ν) in seconds

def format_scientific(number):
    """Formats a number in scientific notation (e.g., 3.00 × 10^8)."""
    if number == 0:
        return "0"
    exponent = int(np.floor(np.log10(abs(number))))
    coefficient = number / (10 ** exponent)
    return f"{coefficient:.2f} × 10^{exponent}"

def validate_input(values_str):
    """Validates and converts input string to a list of floats."""
    try:
        values = list(map(float, values_str.split()))
        if any(val <= 0 for val in values):  # Ensure values are positive
            messagebox.showerror("Invalid Input", "Values must be positive numbers.")
            return None
        return values
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter numbers separated by spaces.")
        return None

def add_reading():
    """Adds wavelength and frequency readings to the lists."""
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

    # Convert wavelength from nm to meters and frequency from THz to Hz
    x_values = [x * 1e-9 for x in x_values]  # Convert nm to meters
    y_values = [y * 1e12 for y in y_values]  # Convert THz to Hz

    # Convert frequency to 1/frequency
    y_values = [1 / y for y in y_values]  # Convert frequency to 1/frequency

    # Add the readings to the lists
    x_readings.append(x_values)
    y_readings.append(y_values)

    # Display the input values in the label
    input_values_label.config(text=f"Added Wavelengths (m): {x_values}\nAdded 1/Frequencies (s): {y_values}")

def plot_graph():
    """Plots the wavelength vs 1/frequency graph."""
    global canvas

    if not x_readings or not y_readings:
        messagebox.showerror("No Data", "No readings to plot. Please add readings first.")
        return

    # Create a figure and plot the graph with dark mode
    with plt.style.context('dark_background'):
        fig, ax = plt.subplots(figsize=(7, 5))
        for x_values, y_values in zip(x_readings, y_readings):
            ax.plot(x_values, y_values, marker='o', linestyle='-', label=f'Reading {x_readings.index(x_values) + 1}')

        ax.set_xlabel('Wavelength (m)', color='white')
        ax.set_ylabel('1/Frequency (s)', color='white')
        ax.set_title('Wavelength vs 1/Frequency Graph', color='white')
        ax.grid(True, linestyle='--', alpha=0.7, color='gray')
        ax.legend()

    # Clear the previous canvas if it exists
    if canvas:
        canvas.get_tk_widget().pack_forget()
        canvas.get_tk_widget().destroy()

    # Embed the figure in Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.draw()
    canvas.get_tk_widget().pack()

def calculate_speed_of_light():
    """Calculates the speed of light using the slope of λ vs. 1/ν."""
    if not x_readings or not y_readings:
        messagebox.showerror("No Data", "No readings to calculate. Please add readings first.")
        return

    speeds_of_light = []
    for x_values, y_values in zip(x_readings, y_readings):
        if len(x_values) < 2 or len(y_values) < 2:
            messagebox.showerror("Insufficient Data", "At least two points are required to calculate the slope.")
            return
        slope, _ = np.polyfit(x_values, y_values, 1)
        speed_of_light = 1 / slope  # Speed of light is the inverse of the slope
        speeds_of_light.append(speed_of_light)

    # Format the speeds of light in scientific notation
    formatted_speeds = [format_scientific(speed) for speed in speeds_of_light]
    slope_label.config(text=f"Calculated Speed of Light (m/s): {', '.join(formatted_speeds)}")

# Create the main window
window = tk.Tk()
window.title("Speed of Light Calculator")
window.configure(background='#121212')  # Dark background

# Create input fields and labels
wavelength_label = tk.Label(window, text="Enter wavelength of light (in nm) separated by spaces:", bg='#121212', fg='white')
wavelength_label.pack()

wavelength_entry = tk.Entry(window, width=40, bg='#1E1E1E', fg='white', insertbackground='white')
wavelength_entry.pack()

frequency_label = tk.Label(window, text="Enter frequency of light (in THz) separated by spaces:", bg='#121212', fg='white')
frequency_label.pack()

frequency_entry = tk.Entry(window, width=40, bg='#1E1E1E', fg='white', insertbackground='white')
frequency_entry.pack()

# Button to add readings
add_button = tk.Button(window, text="Add Reading", command=add_reading, bg='#333333', fg='white')
add_button.pack()

# Button to plot the graph
plot_button = tk.Button(window, text="Plot Graph", command=plot_graph, bg='#006400', fg='white')
plot_button.pack()

# Button to calculate the speed of light
slope_button = tk.Button(window, text="Calculate Speed of Light", command=calculate_speed_of_light, bg='#8B0000', fg='white')
slope_button.pack()

# Label to show the input values
input_values_label = tk.Label(window, text="", justify=tk.LEFT, bg='#121212', fg='white')
input_values_label.pack()

# Label to show the calculated speed of light
slope_label = tk.Label(window, text="", justify=tk.LEFT, bg='#121212', fg='white')
slope_label.pack()

# Initialize the canvas variable
canvas = None

# Start the Tkinter event loop
window.mainloop()