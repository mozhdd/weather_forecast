import sys
from PyQt5.QtWidgets import QApplication

from gui.interface import WeatherGui


if __name__ == '__main__':

    app = QApplication(sys.argv)
    config = r'weather_config.ini'
    ex = WeatherGui(config)
    sys.exit(app.exec_())
