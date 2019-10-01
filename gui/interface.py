import sys
from datetime import datetime
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QMessageBox, \
    QErrorMessage, QLineEdit, QLabel, QCheckBox, QRadioButton, QButtonGroup, \
    QVBoxLayout
from PyQt5.QtCore import QCoreApplication, pyqtSlot
from PyQt5 import QtCore, QtWidgets

from gui.select_location import SelectLocationDlg
from weather_forecast import WeatherForecast
from model.weather_data import WeatherData


class WeatherGui(QWidget):
    def __init__(self):
        super().__init__()
        self.weather_client = WeatherForecast()
        self.weather_data = None
        self._init_ui()

    def _init_ui(self):
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
        self.city_tb.setText('London')

        self.country_tb = QLineEdit(self)
        self.country_tb.move(245, 10)
        self.country_tb.resize(120, 20)
        self.country_tb.setText('GB')

        self.weather_tb = QLineEdit(self)
        self.weather_tb.move(20, 60)
        self.weather_tb.resize(500, 40)
        self.weather_tb.setDisabled(True)

        self.update_btn = QPushButton('Update', self)
        self.update_btn.clicked.connect(self._on_update_forecast)
        self.update_btn.resize(500, 40)
        self.update_btn.move(20, 110)

        self.rb_c = QRadioButton('C', self)
        self.rb_c.move(450, 10)
        self.rb_c.setChecked(True)

        self.rb_f = QRadioButton('F', self)
        self.rb_f.move(450, 30)
        self.button_group = QButtonGroup()
        self.button_group.addButton(self.rb_c)
        self.button_group.addButton(self.rb_f)
        self.button_group.buttonClicked.connect(self._on_temp_units_change)

        self.show()

    def _on_temp_units_change(self, btn):
        self.weather_client.temp_units = btn.text()
        self.weather_tb.setText(self._prepare_str_forecast())

    def _location(self):
        return self.city_tb.text().strip(), self.country_tb.text().strip()

    def _on_update_forecast_old(self):
        ok, fcast_mess = self.weather_client.get_forecast(*self._location())
        if ok:
            self.weather_tb.setText(fcast_mess)
        else:
            QMessageBox.critical(self, 'Error', 'Error: ' + fcast_mess)

    def _on_update_forecast(self):
        ok, data = self.weather_client.find_request(*self._location())
        if not ok:
            QMessageBox.critical(self, 'Error', 'Error: ' + data)
        else:
            if data['count'] == 0:
                QMessageBox.critical(self, 'Error', 'Error: City not found')
            elif data['count'] == 1:
                self.weather_data = self._parse_weather_data(data['list'][0])
            else:
                locations = ['{0}, {1}. Geo coords {2}'.format(
                    loc['name'], loc['sys']['country'],
                    str(list(loc['coord'].values()))) for loc in data['list']]

                ex = SelectLocationDlg(locations)
                ex.setAttribute(QtCore.Qt.WA_DeleteOnClose)
                idx = ex.idx if ex.exec_() == QtWidgets.QDialog.Accepted else\
                    None
                if idx:
                    self.weather_data = self._parse_weather_data(
                        data['list'][idx])

            self.weather_tb.setText(self._prepare_str_forecast())
            if self.weather_data:
                self.country_tb.setText(self.weather_data.country)

    def _parse_weather_data(self, data):
        temp = data['main']['temp']
        descript = data['weather'][0]['description']
        city = data['name']
        country = data['sys']['country']

        return WeatherData(datetime.now(), temp, descript, city, country)

    def _prepare_str_forecast(self):
        if self.weather_data:
            res = self.weather_data.get_str_weather(
                self.weather_client.temp_units)
            return res
        else:
            return ''


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = WeatherGui()
    sys.exit(app.exec_())
