import matplotlib.pyplot as plt
import numpy as np

def validate_input(prompt):
    while True:
        try:
            values = list(map(float, input(prompt).split()))
            return values
        except ValueError:
            print("Invalid input! Please enter numbers separated by spaces.")

# Get user input
x_values = validate_input("Enter the wavelength of light (in nm) separated by spaces: ")
y_values = validate_input("Enter the frequency of light (in Hz) separated by spaces: ")

# Ensure input lengths match
if len(x_values) != len(y_values):
    print("Error: The number of wavelength and frequency values should be the same.")
else:
    # Convert wavelength from nm to meters
    x_meters = [x * 1e-9 for x in x_values]  # Convert nm to meters
    c = 3.0e8  # Speed of light in m/s

    # Compute expected frequency using c = λ * f
    expected_y_values = [c / x for x in x_meters]

    # Calculate deviation percentage
    deviations = [abs((y - y_exp) / y_exp) * 100 for y, y_exp in zip(y_values, expected_y_values)]
    max_deviation = max(deviations)

    # Calculate slope using linear regression (least squares)
    slope, intercept = np.polyfit(x_values, y_values, 1)

    # Alternative: Calculate slope using first and last points
    slope_manual = (y_values[-1] - y_values[0]) / (x_values[-1] - x_values[0])

    # Create the plot
    plt.figure(figsize=(8, 5))
    plt.scatter(x_values, y_values, color='b', label='User Data', marker='o')  # User input points
    plt.plot(x_values, expected_y_values, linestyle='--', color='gray', label='Expected c = λ * f')  # Expected relation

    # Labels and title
    plt.xlabel('Wavelength (nm)')
    plt.ylabel('Frequency (Hz)')
    plt.title('Wavelength vs Frequency Relationship')

    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()

    # Print slope and warning if deviation is significant
    print(f"📏 Slope of the graph (Linear Fit): {slope:.2e} Hz/nm")
    print(f"📏 Slope of the graph (Manual Calc): {slope_manual:.2e} Hz/nm")

    if max_deviation > 5:  # Allow up to 5% deviation
        print(f"⚠️ Warning: The values deviate from c = λ * f by up to {max_deviation:.2f}%.")

    # Show the plot
    plt.show()
