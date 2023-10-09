from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QComboBox, QCompleter, QLineEdit
from PyQt5.uic import loadUi
import sys
import requests
import json
import time

api_key = '960001ee3cd72d2a0e47e49f2c1c13f5'

class WeatherApp(QMainWindow):
    def __init__(self):
        super(WeatherApp, self).__init__()
        loadUi("main.ui", self)

        # Create a QComboBox for city selection
        self.cityComboBox = self.findChild(QComboBox, "CityComboBox")

        # Create a QLineEdit and set it as the line edit for the QComboBox
        self.cityLineEdit = QLineEdit(self)
        self.cityComboBox.setLineEdit(self.cityLineEdit)

        self.city_data = self.load_or_retrieve_city_data()

        # Extract city names from the data
        city_names = [f"{city['name']}, {city['country']}" for city in self.city_data]

        # Create a QCompleter and associate it with the QLineEdit
        completer = QCompleter(city_names, self)
        completer.setCaseSensitivity(False)  # Make suggestions case-insensitive
        self.cityLineEdit.setCompleter(completer)

        # Assign data to the QComboBox
        self.cityComboBox.addItems(city_names)

        # Connect the button click event to a function
        self.Check_button.clicked.connect(self.check_city_weather)


    def check_city_weather(self):
        # Get the selected city from the QComboBox
        selected_city = self.cityComboBox.currentText()

        if selected_city:
            weather_data = requests.get(
                f"https://api.openweathermap.org/data/2.5/weather?q={selected_city}&units=metric&APPID={api_key}")

            if weather_data.json().get('cod') == 200:
                weather = weather_data.json()['weather'][0]['main']
                temp = round(weather_data.json()['main']['temp'])
                QMessageBox.information(self, "Weather Information",
                                        f"Weather in {selected_city}: {weather}, Temperature: {temp}°C")
            else:
                QMessageBox.warning(self, "Error", "City not found!")
        else:
            QMessageBox.warning(self, "Error", "Please select a city from the list.")

    def load_or_retrieve_city_data(self):
        # Cache expiration time (in seconds)
        CACHE_EXPIRATION = 3600  # 1 hour

        # Cache city data in memory if it's not already cached
        current_time = int(time.time())
        if (
                not hasattr(self, "city_data_cache")
                or current_time - self.city_data_cache.get("timestamp", 0) > CACHE_EXPIRATION
        ):
            json_file_path = 'staticresources/city_data.json'

            try:
                with open(json_file_path, 'r', encoding='utf-8') as json_file:
                    city_data = json.load(json_file)
                # Cache the data
                self.city_data_cache = {"data": city_data, "timestamp": current_time}
            except Exception as e:
                # Handle the exception (e.g., show an error message)
                print(f"Error loading city data: {str(e)}")
                # Use the previously cached data if available
                city_data = self.city_data_cache.get("data", [])
        else:
            # Use the cached data
            city_data = self.city_data_cache.get("data", [])

        return city_data

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WeatherApp()
    window.show()
    app.exec_()

