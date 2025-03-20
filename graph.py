# import tkinter as tk
# from tkinter import messagebox
# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# # Initialize lists to store readings
# x_readings = []
# y_readings = []

# def format_scientific(number):
#     """Formats numbers in scientific notation"""
#     if number == 0:
#         return "0"
#     exponent = int(np.floor(np.log10(abs(number))))
#     coefficient = number / (10 ** exponent)
#     return f"{coefficient:.2f} × 10^{exponent}"

# def validate_input(values_str):
#     """Validates and converts input string to a NumPy array"""
#     try:
#         values = np.array(list(map(float, values_str.split())))
#         if np.any(values <= 0):  # Check for non-positive values
#             messagebox.showerror("Invalid Input", "Values must be positive numbers.")
#             return None
#         return values
#     except ValueError:
#         messagebox.showerror("Invalid Input", "Please enter numbers separated by spaces.")
#         return None

# def add_reading():
#     """Adds wavelength and frequency readings to the list"""
#     global x_readings, y_readings

#     x_input = wavelength_entry.get()
#     y_input = frequency_entry.get()

#     if not x_input or not y_input:
#         messagebox.showerror("Input Error", "Please enter values in both fields.")
#         return

#     x_values = validate_input(x_input)
#     y_values = validate_input(y_input)

#     if x_values is None or y_values is None:
#         return

#     if len(x_values) != len(y_values):
#         messagebox.showerror("Input Error", "The number of wavelength and frequency values should be the same.")
#         return

#     # Convert wavelength from nm to meters
#     x_values = (x_values * 1e-9).tolist()  # Convert to meters and make it a Python list
#     y_values = (1 / y_values).tolist()  # Convert frequency to 1/frequency and make it a Python list

#     x_readings.extend(x_values)  # Store as flat list
#     y_readings.extend(y_values)  # Store as flat list

#     # Display the input values
#     input_values_label.config(text=f"Added Wavelengths (m): {', '.join(map(str, x_values))}\n"
#                                    f"Added 1/Frequencies (s): {', '.join(map(str, y_values))}")

# def plot_graph():
#     """Plots the wavelength vs 1/frequency graph with trendlines"""
#     global canvas

#     if not x_readings or not y_readings:
#         messagebox.showerror("No Data", "No readings to plot. Please add readings first.")
#         return

#     # Clear previous canvas
#     if canvas:
#         canvas.get_tk_widget().pack_forget()
#         canvas.get_tk_widget().destroy()
#         canvas = None

#     # Create a figure with dark mode
#     with plt.style.context('dark_background'):
#         fig, ax = plt.subplots(figsize=(7, 5))
#         ax.plot(x_readings, y_readings, 'wo', label="Experimental Data")  # White circles for data points

#         # Define different polynomial degrees and colors for trendlines
#         degrees = [1, 2, 3]
#         colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']  # Red, Teal, Blue
#         line_styles = ['-', '--', ':']  # Solid, Dashed, Dotted

#         # Convert to numpy arrays
#         x_arr = np.array(x_readings)
#         y_arr = np.array(y_readings)

#         # Generate trendlines for different degrees
#         x_fit = np.linspace(min(x_arr), max(x_arr), 100)
        
#         for degree, color, ls in zip(degrees, colors, line_styles):
#             try:
#                 # Fit polynomial
#                 coeffs = np.polyfit(x_arr, y_arr, degree)
#                 p = np.poly1d(coeffs)
#                 y_fit = p(x_fit)
                
#                 ax.plot(x_fit, y_fit, color=color, linestyle=ls, 
#                         label=f'Degree {degree} Fit', linewidth=2)
#             except:
#                 messagebox.showwarning("Fit Error", 
#                     f"Could not calculate degree {degree} fit. Not enough data points?")
#                 continue

#         ax.set_xlabel('Wavelength (m)', color="white")
#         ax.set_ylabel('1/Frequency (s)', color="white")
#         ax.set_title('Wavelength vs 1/Frequency with Trendlines', color="white")
#         ax.grid(True, linestyle='--', alpha=0.7, color="gray")
#         ax.legend()

#     # Embed figure in Tkinter window
#     canvas = FigureCanvasTkAgg(fig, master=window)
#     canvas.draw()
#     canvas.get_tk_widget().pack()

# def calculate_speed_of_light():
#     """Calculates speed of light using linear regression"""
#     if not x_readings or not y_readings:
#         messagebox.showerror("No Data", "No readings to calculate. Please add readings first.")
#         return

#     x_arr = np.array(x_readings)
#     y_arr = np.array(y_readings)

#     try:
#         slope, intercept = np.polyfit(x_arr, y_arr, 1)
#         if slope == 0:
#             messagebox.showerror("Error", "Slope is zero - invalid data")
#             return
#         c = 1 / slope
#         formatted_c = format_scientific(c)
#         slope_label.config(text=f"Calculated Speed of Light: {formatted_c} m/s\n"
#                                  f"(Using linear regression)")
#     except:
#         messagebox.showerror("Calculation Error", "Failed to calculate speed of light")

# # GUI Setup
# window = tk.Tk()
# window.title("Speed of Light Calculator with Trendlines")
# window.configure(background='#121212')  # Dark mode

# # Widgets
# wavelength_label = tk.Label(window, text="Enter wavelength (nm):", bg='#121212', fg='white')
# wavelength_entry = tk.Entry(window, width=40, bg='#1E1E1E', fg='white')
# frequency_label = tk.Label(window, text="Enter frequency (Hz):", bg='#121212', fg='white')
# frequency_entry = tk.Entry(window, width=40, bg='#1E1E1E', fg='white')

# add_button = tk.Button(window, text="Add Reading", command=add_reading, bg='#333333', fg='white')
# plot_button = tk.Button(window, text="Plot Graph", command=plot_graph, bg='#006400', fg='white')
# slope_button = tk.Button(window, text="Calculate c", command=calculate_speed_of_light, bg='#8B0000', fg='white')

# input_values_label = tk.Label(window, text="", bg='#121212', fg='white')
# slope_label = tk.Label(window, text="", bg='#121212', fg='white')

# # Layout
# wavelength_label.pack(pady=5)
# wavelength_entry.pack(pady=5)
# frequency_label.pack(pady=5)
# frequency_entry.pack(pady=5)
# add_button.pack(pady=10)
# plot_button.pack(pady=5)
# slope_button.pack(pady=10)
# input_values_label.pack()
# slope_label.pack()

# canvas = None

# # Start the Tkinter event loop
# window.mainloop()