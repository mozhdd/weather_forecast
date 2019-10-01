import sys
from PyQt5.QtWidgets import QApplication

from gui.interface import WeatherGui


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = WeatherGui()
    sys.exit(app.exec_())
