from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QComboBox, QCompleter, QLineEdit
from PyQt5.uic import loadUi
import sys
import requests
import json

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

        # Load city data from JSON file in the 'staticresources' folder
        json_file_path = 'staticresources/city_data.json'

        with open(json_file_path, 'r', encoding='utf-8') as json_file:
            self.city_data = json.load(json_file)

        # Extract city names from the data
        city_names = [city["name"] for city in self.city_data]

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WeatherApp()
    window.show()
    app.exec_()

