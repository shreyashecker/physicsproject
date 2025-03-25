from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
import matplotlib.pyplot as plt
import numpy as np
import os

# Set dark mode for the app
Window.clearcolor = get_color_from_hex('#121212')  # Dark background

class MobileSpeedOfLightApp(App):
    def build(self):
        self.title = "Speed of Light Calculator"
        self.x_readings = []  # Wavelength (λ) in meters
        self.y_readings = []  # 1/Frequency (1/ν) in seconds

        # Main layout - ScrollView for mobile devices
        self.scroll_layout = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        self.main_layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10), size_hint_y=None)
        self.main_layout.bind(minimum_height=self.main_layout.setter('height'))
        
        # Header
        header = Label(text="Speed of Light Calculator", font_size=dp(24), bold=True, 
                      size_hint_y=None, height=dp(50), color=get_color_from_hex('#4FC3F7'))
        self.main_layout.add_widget(header)

        # Input section
        input_section = BoxLayout(orientation='vertical', spacing=dp(10), size_hint_y=None, height=dp(200))
        
        # Wavelength input
        wavelength_label = Label(text="Wavelength (nm):", size_hint_y=None, height=dp(20), 
                               color=get_color_from_hex('#B3E5FC'))
        self.wavelength_input = TextInput(
            hint_text="e.g. 400 500 600", 
            multiline=False, 
            size_hint_y=None, 
            height=dp(40),
            background_color=get_color_from_hex('#424242'),
            foreground_color=get_color_from_hex('#FFFFFF'),
            hint_text_color=get_color_from_hex('#BDBDBD')
        )
        
        # Frequency input
        frequency_label = Label(text="Frequency (THz):", size_hint_y=None, height=dp(20), 
                              color=get_color_from_hex('#B3E5FC'))
        self.frequency_input = TextInput(
            hint_text="e.g. 750 600 500", 
            multiline=False, 
            size_hint_y=None, 
            height=dp(40),
            background_color=get_color_from_hex('#424242'),
            foreground_color=get_color_from_hex('#FFFFFF'),
            hint_text_color=get_color_from_hex('#BDBDBD')
        )
        
        input_section.add_widget(wavelength_label)
        input_section.add_widget(self.wavelength_input)
        input_section.add_widget(frequency_label)
        input_section.add_widget(self.frequency_input)
        self.main_layout.add_widget(input_section)

        # Button section
        button_section = BoxLayout(orientation='vertical', spacing=dp(10), size_hint_y=None, height=dp(150))
        
        self.add_button = Button(
            text="Add Reading", 
            size_hint_y=None, 
            height=dp(40),
            background_color=get_color_from_hex('#0277BD'),
            background_normal=''
        )
        self.plot_button = Button(
            text="Plot Graph", 
            size_hint_y=None, 
            height=dp(40),
            background_color=get_color_from_hex('#0288D1'),
            background_normal=''
        )
        self.calculate_button = Button(
            text="Calculate Speed", 
            size_hint_y=None, 
            height=dp(40),
            background_color=get_color_from_hex('#039BE5'),
            background_normal=''
        )
        
        button_section.add_widget(self.add_button)
        button_section.add_widget(self.plot_button)
        button_section.add_widget(self.calculate_button)
        self.main_layout.add_widget(button_section)

        # Results section with scrollable containers
        results_container = BoxLayout(orientation='vertical', spacing=dp(10), size_hint_y=None)
        
        # Current Readings ScrollView
        readings_scroll_container = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(150))
        readings_label = Label(text="Current Readings:", size_hint_y=None, height=dp(20), 
                             color=get_color_from_hex('#B3E5FC'))
        readings_scroll_container.add_widget(readings_label)
        
        readings_scroll = ScrollView(size_hint=(1, None), height=dp(130))
        self.input_values_label = Label(
            text="No readings added yet", 
            size_hint_y=None, 
            color=get_color_from_hex('#E1F5FE'),
            halign='left',
            valign='top',
            text_size=(Window.width-dp(20), None)
        )
        self.input_values_label.bind(
            texture_size=lambda instance, size: setattr(self.input_values_label, 'height', size[1])
        )
        readings_scroll.add_widget(self.input_values_label)
        readings_scroll_container.add_widget(readings_scroll)
        
        # Speed Results ScrollView
        speed_scroll_container = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(150))
        speed_label = Label(text="Speed Results:", size_hint_y=None, height=dp(20), 
                          color=get_color_from_hex('#B3E5FC'))
        speed_scroll_container.add_widget(speed_label)
        
        speed_scroll = ScrollView(size_hint=(1, None), height=dp(130))
        self.speed_result_label = Label(
            text="Speed will appear here", 
            size_hint_y=None, 
            color=get_color_from_hex('#E1F5FE'),
            halign='left',
            valign='top',
            text_size=(Window.width-dp(20), None)
        )
        self.speed_result_label.bind(
            texture_size=lambda instance, size: setattr(self.speed_result_label, 'height', size[1])
        )
        speed_scroll.add_widget(self.speed_result_label)
        speed_scroll_container.add_widget(speed_scroll)
        
        # Add both scroll containers to results
        results_container.add_widget(readings_scroll_container)
        results_container.add_widget(speed_scroll_container)
        
        # Calculate minimum height for results container
        results_container.bind(minimum_height=results_container.setter('height'))
        self.main_layout.add_widget(results_container)

        # Image widget for displaying the plot - Fixed height
        self.plot_image = Image(
            size_hint_y=None, 
            height=dp(300),
            allow_stretch=True,
            keep_ratio=True
        )
        # Initially hide the plot image
        self.plot_image.opacity = 0
        self.main_layout.add_widget(self.plot_image)

        # Add main layout to scroll view
        self.scroll_layout.add_widget(self.main_layout)

        # Bind buttons to functions
        self.add_button.bind(on_press=self.add_reading)
        self.plot_button.bind(on_press=self.plot_graph)
        self.calculate_button.bind(on_press=self.calculate_speed_of_light)

        return self.scroll_layout

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
        display_text = ""
        for i, (x_vals, y_vals) in enumerate(zip(self.x_readings, self.y_readings)):
            display_text += f"\nReading {i+1}:\n"
            display_text += f"λ (m): {', '.join([f'{x:.2e}' for x in x_vals])}\n"
            display_text += f"1/ν (s): {', '.join([f'{y:.2e}' for y in y_vals])}\n"
        
        self.input_values_label.text = display_text.strip()
        self.input_values_label.texture_update()

    def plot_graph(self, instance):
        """Plots the wavelength vs 1/frequency graph and displays it in the Image widget."""
        if not self.x_readings or not self.y_readings:
            self.show_popup("No Data", "No readings to plot. Please add readings first.")
            return

        # Create a figure and plot the graph with dark mode
        with plt.style.context('dark_background'):
            fig, ax = plt.subplots(figsize=(6, 5))  # Smaller size for mobile
            for x_values, y_values in zip(self.x_readings, self.y_readings):
                ax.plot(x_values, y_values, marker='o', linestyle='-', label=f'Reading {self.x_readings.index(x_values) + 1}')

            ax.set_xlabel('Wavelength (m)', color='white')
            ax.set_ylabel('1/Frequency (s)', color='white')
            ax.set_title('Wavelength vs 1/Frequency', color='white')
            ax.grid(True, linestyle='--', alpha=0.7, color='gray')
            ax.legend()

        # Save the plot as an image
        plot_filename = "plot.png"
        fig.savefig(plot_filename, bbox_inches='tight', facecolor='#121212', dpi=100)
        plt.close(fig)

        # Load the image into the Kivy Image widget
        self.plot_image.source = plot_filename
        self.plot_image.reload()
        self.plot_image.opacity = 1  # Make the image visible

    def calculate_speed_of_light(self, instance):
        """Calculates the speed of light using the slope of λ vs. 1/ν."""
        if not self.x_readings or not self.y_readings:
            self.show_popup("No Data", "No readings to calculate. Please add readings first.")
            return

        speeds_of_light = []
        for i, (x_values, y_values) in enumerate(zip(self.x_readings, self.y_readings)):
            if len(x_values) < 2 or len(y_values) < 2:
                self.show_popup("Insufficient Data", "At least two points are required to calculate the slope.")
                return
            slope, _ = np.polyfit(x_values, y_values, 1)
            speed_of_light = 1 / slope  # Speed of light is the inverse of the slope
            speeds_of_light.append(speed_of_light)

        # Format the results
        result_text = ""
        for i, speed in enumerate(speeds_of_light):
            formatted_speed = self.format_scientific(speed)
            error_percent = abs((speed - 2.998e8) / 2.998e8) * 100
            result_text += f"\nReading {i+1}: {formatted_speed} m/s\n"
            result_text += f"Error: {error_percent:.2f}%\n"
        
        # Add average if multiple readings
        if len(speeds_of_light) > 1:
            avg_speed = np.mean(speeds_of_light)
            avg_error = abs((avg_speed - 2.998e8) / 2.998e8) * 100
            result_text += f"\nAverage: {self.format_scientific(avg_speed)} m/s\n"
            result_text += f"Avg Error: {avg_error:.2f}%"
        
        self.speed_result_label.text = result_text.strip()
        self.speed_result_label.texture_update()

    def show_popup(self, title, message):
        """Displays a popup with the given title and message."""
        popup_layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        popup_label = Label(text=message, size_hint_y=None, height=dp(80), color=get_color_from_hex('#E1F5FE'))
        popup_label.bind(size=popup_label.setter('text_size'))
        popup_button = Button(
            text="OK", 
            size_hint_y=None, 
            height=dp(40),
            background_color=get_color_from_hex('#0288D1'),
            background_normal=''
        )

        popup_layout.add_widget(popup_label)
        popup_layout.add_widget(popup_button)

        popup = Popup(
            title=title, 
            content=popup_layout, 
            size_hint=(0.8, 0.4),
            title_color=get_color_from_hex('#4FC3F7'),
            separator_color=get_color_from_hex('#0288D1')
        )
        popup_button.bind(on_press=popup.dismiss)
        popup.open()

# Run the app
if __name__ == "__main__":
    MobileSpeedOfLightApp().run()