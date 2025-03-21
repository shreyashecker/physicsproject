from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.core.window import Window
import matplotlib.pyplot as plt
import numpy as np
import os

# Set dark mode for the app
Window.clearcolor = (0.1, 0.1, 0.1, 1)  # Dark background

class SpeedOfLightApp(App):
    def build(self):
        self.title = "Speed of Light Calculator"
        self.x_readings = []  # Wavelength (λ) in meters
        self.y_readings = []  # 1/Frequency (1/ν) in seconds

        # Main layout
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Input fields
        self.wavelength_input = TextInput(hint_text="Enter wavelength (nm) separated by spaces", multiline=False, size_hint_y=None, height=40)
        self.frequency_input = TextInput(hint_text="Enter frequency (THz) separated by spaces", multiline=False, size_hint_y=None, height=40)

        # Buttons
        self.add_button = Button(text="Add Reading", size_hint_y=None, height=40)
        self.plot_button = Button(text="Plot Graph", size_hint_y=None, height=40)
        self.calculate_button = Button(text="Calculate Speed of Light", size_hint_y=None, height=40)

        # Labels for displaying results
        self.input_values_label = Label(text="Input values will appear here", size_hint_y=None, height=60)
        self.speed_label = Label(text="Calculated speed of light will appear here", size_hint_y=None, height=60)

        # Image widget for displaying the plot
        self.plot_image = Image(size_hint_y=None, height=300)

        # Add widgets to the layout
        self.layout.add_widget(self.wavelength_input)
        self.layout.add_widget(self.frequency_input)
        self.layout.add_widget(self.add_button)
        self.layout.add_widget(self.plot_button)
        self.layout.add_widget(self.calculate_button)
        self.layout.add_widget(self.input_values_label)
        self.layout.add_widget(self.speed_label)
        self.layout.add_widget(self.plot_image)

        # Bind buttons to functions
        self.add_button.bind(on_press=self.add_reading)
        self.plot_button.bind(on_press=self.plot_graph)
        self.calculate_button.bind(on_press=self.calculate_speed_of_light)

        return self.layout

    def format_scientific(self, number):
        """Formats a number in scientific notation (e.g., 3.00 × 10^8)."""
        if number == 0:
            return "0"
        exponent = int(np.floor(np.log10(abs(number))))
        coefficient = number / (10 ** exponent)
        return f"{coefficient:.2f} × 10^{exponent}"

    def validate_input(self, values_str):
        """Validates and converts input string to a list of floats."""
        try:
            values = list(map(float, values_str.split()))
            if any(val <= 0 for val in values):  # Ensure values are positive
                self.show_popup("Invalid Input", "Values must be positive numbers.")
                return None
            return values
        except ValueError:
            self.show_popup("Invalid Input", "Please enter numbers separated by spaces.")
            return None

    def add_reading(self, instance):
        """Adds wavelength and frequency readings to the lists."""
        x_input = self.wavelength_input.text
        y_input = self.frequency_input.text

        x_values = self.validate_input(x_input)
        y_values = self.validate_input(y_input)

        if x_values is None or y_values is None:
            return

        if len(x_values) != len(y_values):
            self.show_popup("Input Error", "The number of wavelength and frequency values should be the same.")
            return

        # Convert wavelength from nm to meters and frequency from THz to Hz
        x_values = [x * 1e-9 for x in x_values]  # Convert nm to meters
        y_values = [y * 1e12 for y in y_values]  # Convert THz to Hz

        # Convert frequency to 1/frequency
        y_values = [1 / y for y in y_values]  # Convert frequency to 1/frequency

        # Add the readings to the lists
        self.x_readings.append(x_values)
        self.y_readings.append(y_values)

        # Display the input values in the label
        self.input_values_label.text = f"Added Wavelengths (m): {x_values}\nAdded 1/Frequencies (s): {y_values}"

    def plot_graph(self, instance):
        """Plots the wavelength vs 1/frequency graph and displays it in the Image widget."""
        if not self.x_readings or not self.y_readings:
            self.show_popup("No Data", "No readings to plot. Please add readings first.")
            return

        # Create a figure and plot the graph with dark mode
        with plt.style.context('dark_background'):
            fig, ax = plt.subplots(figsize=(9, 8))
            for x_values, y_values in zip(self.x_readings, self.y_readings):
                ax.plot(x_values, y_values, marker='o', linestyle='-', label=f'Reading {self.x_readings.index(x_values) + 1}')

            ax.set_xlabel('Wavelength (m)', color='white')
            ax.set_ylabel('1/Frequency (s)', color='white')
            ax.set_title('Wavelength vs 1/Frequency Graph', color='white')
            ax.grid(True, linestyle='--', alpha=0.7, color='gray')
            ax.legend()

        # Save the plot as an image
        plot_filename = "plot.png"
        fig.savefig(plot_filename, bbox_inches='tight', facecolor='#121212')
        plt.close(fig)

        # Load the image into the Kivy Image widget
        self.plot_image.source = plot_filename
        self.plot_image.reload()

    def calculate_speed_of_light(self, instance):
        """Calculates the speed of light using the slope of λ vs. 1/ν."""
        if not self.x_readings or not self.y_readings:
            self.show_popup("No Data", "No readings to calculate. Please add readings first.")
            return

        speeds_of_light = []
        for x_values, y_values in zip(self.x_readings, self.y_readings):
            if len(x_values) < 2 or len(y_values) < 2:
                self.show_popup("Insufficient Data", "At least two points are required to calculate the slope.")
                return
            slope, _ = np.polyfit(x_values, y_values, 1)
            speed_of_light = 1 / slope  # Speed of light is the inverse of the slope
            speeds_of_light.append(speed_of_light)

        # Format the speeds of light in scientific notation
        formatted_speeds = [self.format_scientific(speed) for speed in speeds_of_light]
        self.speed_label.text = f"Calculated Speed of Light (m/s): {', '.join(formatted_speeds)}"

    def show_popup(self, title, message):
        """Displays a popup with the given title and message."""
        popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        popup_label = Label(text=message, size_hint_y=None, height=40)
        popup_button = Button(text="OK", size_hint_y=None, height=40)

        popup_layout.add_widget(popup_label)
        popup_layout.add_widget(popup_button)

        popup = Popup(title=title, content=popup_layout, size_hint=(0.8, 0.4))
        popup_button.bind(on_press=popup.dismiss)
        popup.open()

# Run the app
if __name__ == "__main__":
    SpeedOfLightApp().run()