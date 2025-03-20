import matplotlib.pyplot as plt

def validate_input(prompt):
    while True:
        try:
            values = list(map(float, input(prompt).split()))
            return values
        except ValueError:
            print("Invalid input! Please enter numbers separated by spaces.")

x_values = validate_input("Enter the  of light (in nm) separated by spaces: ")
y_values = validate_input("Enter the frequency of light (in Hz) separated by spaces: ")

if len(x_values) != len(y_values):
    print("Error: The number of wavelength and frequency values should be the same.")
else:
    # Convert nm to meters for physics validation
    x_meters = [x * 1e-9 for x in x_values]  # Convert nm to m
    c = 3.0e8  # Speed of light in m/s
    valid_relation = all(abs(c - (x * y)) < 1e6 for x, y in zip(x_meters, y_values))

    plt.figure(figsize=(7, 5))
    plt.plot(x_values, y_values, marker='o', linestyle='-', color='r', label='Wavelength vs Frequency')

    plt.xlabel('Wavelength (nm)')
    plt.ylabel('Frequency (Hz)')
    plt.title('Wavelength vs Frequency Graph')

    plt.grid(True)
    plt.legend()

    if not valid_relation:
        print("Warning: The values do not follow the expected c = λ * f relationship.")

    plt.show()
