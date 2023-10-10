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

        # Retrieve distinct city data with IDs from the database
        self.city_data = self.retrieve_city_data()

        self.conn.close()

        # Create a dictionary to store city data where ID is the key
        self.city_data_dict = {city_id: (city_name, country_code) for city_id, city_name, country_code in self.city_data}

        # Populate the ComboBox with city names
        self.populate_combobox()

        # Create a QCompleter and associate it with the QLineEdit
        completer = QCompleter(self.city_names, self)
        completer.setCaseSensitivity(Qt.CaseInsensitive)  # Make suggestions case-insensitive
        self.cityLineEdit.setCompleter(completer)

        # Connect the button click event to a function
        self.Check_button.clicked.connect(self.check_city_weather)

    def populate_combobox(self):
        self.city_names = []  # Store city names for QCompleter
        self.cityComboBox.clear()  # Clear the ComboBox before adding items

        for city_id, (city_name, country_code) in self.city_data_dict.items():
            display_text = f"{city_name}, {country_code}"  # Displayed text in ComboBox
            self.cityComboBox.addItem(display_text)
            self.city_names.append(display_text)

    def check_city_weather(self):
        # Get the selected index from the QComboBox
        selected_index = self.cityComboBox.currentIndex()

        if selected_index != -1:
            # Retrieve the associated city ID for the selected index
            selected_city_id = list(self.city_data_dict.keys())[selected_index]
            print(selected_city_id)

            weather_data = requests.get(
                f"https://api.openweathermap.org/data/2.5/weather?id={selected_city_id}&units=metric&APPID={api_key}")

            if weather_data.json().get('cod') == 200:
                selected_text = self.cityComboBox.currentText()
                weather = weather_data.json()['weather'][0]['main']
                temp = round(weather_data.json()['main']['temp'])
                QMessageBox.information(self, "Weather Information",
                                        f"Weather in {selected_text}: {weather}, Temperature: {temp}°C")
            else:
                QMessageBox.warning(self, "Error", "City not found!")
        else:
            QMessageBox.warning(self, "Error", "Please select a city from the list.")

    def retrieve_city_data(self):
        # Retrieve distinct city-country combinations with IDs from the database
        self.cursor.execute("SELECT id, name, country FROM cities GROUP BY name, country")
        return self.cursor.fetchall()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WeatherApp()
    window.show()
    app.exec_()
