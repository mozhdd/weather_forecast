import sys
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QMessageBox, \
    QErrorMessage, QLineEdit, QLabel
from PyQt5.QtCore import QCoreApplication

from weather_forecast import WeatherForecast


class WeatherGui(QWidget):
    def __init__(self):
        super().__init__()

        self.weather_tb = None
        self.update_btn = None

        self.weather_client = WeatherForecast()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Weather Forecast')
        self.setGeometry(300, 300, 600, 400)

        city_lbl = QLabel(self)
        city_lbl.setText('City:')
        city_lbl.move(20, 10)

        country_lbl = QLabel(self)
        country_lbl.setText('Country:')
        country_lbl.move(190, 10)

        self.city_tb = QLineEdit(self)
        self.city_tb.move(50, 10)
        self.city_tb.resize(120, 20)
        self.city_tb.setDisabled(True)
        self.city_tb.setText('London')

        self.country_tb = QLineEdit(self)
        self.country_tb.move(245, 10)
        self.country_tb.resize(120, 20)
        self.country_tb.setDisabled(True)
        self.country_tb.setText('GB')

        self.weather_tb = QLineEdit(self)
        self.weather_tb.move(20, 60)
        self.weather_tb.resize(345, 40)
        self.weather_tb.setDisabled(True)

        self.update_btn = QPushButton('Update', self)
        self.update_btn.clicked.connect(self.update_forecast)
        self.update_btn.resize(345, 40)
        # self.update_btn.resize(self.update_btn.sizeHint())
        self.update_btn.move(20, 110)

        self.show()

    def init_location(self):
        pass

    def update_forecast(self):
        ok, fcast_mess = self.weather_client.get_forecast()
        if ok:
            self.weather_tb.setText(fcast_mess)
        else:
            QMessageBox.critical(self, 'Error', 'Error: ' + fcast_mess)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = WeatherGui()
    sys.exit(app.exec_())
