import sys
from datetime import datetime
from PyQt5.QtWidgets import QWidget, QPushButton, QApplication, QMessageBox, \
    QLineEdit, QLabel, QRadioButton, QButtonGroup, QToolTip
from PyQt5 import QtCore, QtWidgets, QtGui


from gui.select_location import SelectLocationDlg
from weather_forecast import WeatherForecast
from model.weather_data import WeatherData
from updates_handler import PeriodicExecutor


class WeatherGui(QWidget):
    def __init__(self):
        super().__init__()
        self.weather_client = WeatherForecast()
        self.weather_data = None
        self.timer = None
        self.update_time_sec = 30 * 60

        self._init_ui()

    def _init_ui(self):
        self.setWindowTitle('Weather Forecast')
        self.move(300, 300)
        self.setFixedSize(640, 300)

        city_lbl = QLabel(self)
        city_lbl.setText('City:')
        city_lbl.move(20, 12)

        country_lbl = QLabel(self)
        country_lbl.setText('Country:')
        country_lbl.move(190, 12)

        self.city_tb = QLineEdit(self)
        self.city_tb.move(50, 10)
        self.city_tb.resize(120, 20)
        self.city_tb.setText('London')
        self.city_tb.setToolTip("Put city's name here")

        self.country_tb = QLineEdit(self)
        self.country_tb.move(245, 10)
        self.country_tb.resize(120, 20)
        self.country_tb.setText('GB')
        self.country_tb.setToolTip("2-letter country code (ISO3166)")

        self.weather_tb = QLineEdit(self)
        self.weather_tb.move(20, 90)
        self.weather_tb.resize(600, 50)
        self.weather_tb.setDisabled(True)
        self.weather_tb.setFont(QtGui.QFont('SansSerif', 10))

        self.update_btn = QPushButton('Update', self)
        self.update_btn.clicked.connect(self._on_update_forecast)
        self.update_btn.resize(345, 25)
        self.update_btn.move(20, 40)

        self.search_btn = QPushButton('Search', self)
        self.search_btn.clicked.connect(self._on_find_forecast)
        self.search_btn.resize(600, 40)
        self.search_btn.move(20, 150)

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

    def closeEvent(self, event):
        quit_msg = "Are you sure you want to exit?"
        reply = QMessageBox.question(self, 'Message', quit_msg,
                                     QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            if self.timer:
                self.timer.stop()
            event.accept()
        else:
            event.ignore()

    def _on_temp_units_change(self, btn):
        self.weather_client.temp_units = btn.text()
        self.weather_tb.setText(self._prepare_str_forecast())

    def _location(self):
        return self.city_tb.text().strip(), self.country_tb.text().strip()

    def _on_find_forecast(self):
        data = self.weather_client.forecast_from_find_request(*self._location())
        if not data['ok']:
            QMessageBox.critical(self, 'Error', 'Error: ' + data['message'])
        else:
            if data['count'] == 0:
                QMessageBox.critical(self, 'Error', 'Error: City not found')
            elif data['count'] == 1:
                self.weather_data = WeatherData(data['list'][0])
            else:
                locations = ['{0}, {1}. Geo coords {2}'.format(
                    loc['name'], loc['sys']['country'],
                    str(list(loc['coord'].values()))) for loc in data['list']]

                ex = SelectLocationDlg(locations)
                ex.setAttribute(QtCore.Qt.WA_DeleteOnClose)
                idx = ex.idx if ex.exec_() == QtWidgets.QDialog.Accepted else\
                    None
                if idx is not None:
                    self.weather_data = WeatherData(data['list'][idx])

            self.weather_tb.setText(self._prepare_str_forecast())
            if self.weather_data:
                self.country_tb.setText(self.weather_data.country)
                self._start_autoupdate()

    def _on_update_forecast(self):
        if self.weather_data:
            data = self.weather_client.forecast_by_id(
                self.weather_data.city_id)
            if data['ok']:
                self.weather_data = WeatherData(data)
                self.weather_tb.setText(self._prepare_str_forecast())
            else:
                QMessageBox.critical(self, 'Error', 'Error: '+data['message'])

    def _prepare_str_forecast(self):
        if self.weather_data:
            res = self.weather_data.get_str_weather(
                self.weather_client.temp_units)
            return res
        else:
            return ''

    def _start_autoupdate(self):
        self.timer = PeriodicExecutor(interval_sec=self.update_time_sec,
                                      execute=self._on_update_forecast)
        self.timer.start()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = WeatherGui()
    sys.exit(app.exec_())
