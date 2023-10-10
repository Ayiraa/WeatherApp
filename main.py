from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QComboBox, QCompleter, QLineEdit
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi
import sys
import requests
import sqlite3

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

        # Initialize SQLite database and load city data
        self.conn = sqlite3.connect("weather.db")
        self.cursor = self.conn.cursor()

        # Retrieve city names and country codes directly from the database
        self.city_data = self.retrieve_city_data()

        # Extract city names and format them as "City, Country"
        city_names = [f"{name}, {country}" for name, country in self.city_data]

        # Create a QCompleter and associate it with the QLineEdit
        completer = QCompleter(city_names, self)
        completer.setCaseSensitivity(Qt.CaseInsensitive)  # Make suggestions case-insensitive
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

    def retrieve_city_data(self):
        # Retrieve city names and country codes from the database
        self.cursor.execute("SELECT name, country FROM cities")
        return self.cursor.fetchall()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WeatherApp()
    window.show()
    app.exec_()
