import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from collections import namedtuple


Settings = namedtuple('Settings', ['update_time_sec'])


class SettingsUI(QtWidgets.QDialog):
    def __init__(self, update_time_sec):
        super().__init__()
        self.time_sec = update_time_sec
        self.settings = None

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Settings')

        font = QtGui.QFont('Arial', 9)
        vert_lay = QtWidgets.QVBoxLayout(self)

        lbl = QtWidgets.QLabel(self)
        lbl.setText('Update forecast every (sec)')
        lbl.setFont(font)
        self.update_time_sb = QtWidgets.QSpinBox(self)
        self.update_time_sb.setMinimum(1)
        self.update_time_sb.setMaximum(9999999)
        self.update_time_sb.setValue(self.time_sec)

        hor_lay = QtWidgets.QHBoxLayout(self)
        hor_lay.addWidget(lbl)
        hor_lay.addWidget(self.update_time_sb)

        lbl = QtWidgets.QLabel(self)
        lbl.setText('Some other setting parameters could be here.')
        lbl.setFont(font)

        vert_lay.addLayout(hor_lay)
        vert_lay.addWidget(lbl)

        # button box
        self.button_box = QtWidgets.QDialogButtonBox(self)
        self.button_box.setEnabled(True)
        self.button_box.setStandardButtons(
            QtWidgets.QDialogButtonBox.Cancel |
            QtWidgets.QDialogButtonBox.Ok)
        self.button_box.setObjectName("button_box")
        self.button_box.accepted.connect(self.on_accepst)
        self.button_box.rejected.connect(self.on_reject)

        vert_lay.addWidget(self.button_box)

    def on_accepst(self):
        self.settings = Settings(self.update_time_sb.value())
        self.accept()

    def on_reject(self):
        # Define default params
        self.settings = Settings(self.time_sec)
        self.reject()


def _open_settings_dialog():
    app = QtWidgets.QApplication(sys.argv)
    ex = SettingsUI(10)
    ex.setAttribute(QtCore.Qt.WA_DeleteOnClose)

    settings = ex.settings if \
        ex.exec_() == QtWidgets.QDialog.Accepted else None
    return settings


if __name__ == '__main__':
    print(_open_settings_dialog())
