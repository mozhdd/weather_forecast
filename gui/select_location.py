import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from functools import partial


class SelectLocationDlg(QtWidgets.QDialog):
    def __init__(self, locations):
        super().__init__()
        self.idx = None
        self.locations = locations
        self.init_ui()

    def init_ui(self):
        vert_lay = QtWidgets.QVBoxLayout(self)

        lbl = QtWidgets.QLabel(self)
        lbl.setText('Several results were found for a given query. '
                    '\nSelect location.')
        lbl.setFont(QtGui.QFont('SansSerif', 10))
        vert_lay.addWidget(lbl)

        for i, loc in enumerate(self.locations):
            hor_lay = self._ini_item(i, loc)
            vert_lay.addLayout(hor_lay)

    def _ini_item(self, i, mess):

        hor_lay = QtWidgets.QHBoxLayout(self)

        btn = QtWidgets.QPushButton(mess)
        btn.clicked.connect(partial(self.on_clicked, i))

        # lbl = QtWidgets.QLabel(self)
        # lbl.setText(mess)

        hor_lay.addWidget(btn)
        # hor_lay.addWidget(lbl)

        return hor_lay

    def on_clicked(self, idx):
        self.idx = idx
        self.accept()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = SelectLocationDlg(['Moscow, RU. Geo coords [55.7507, 37.6177]',
 'Moscow, US. Geo coords [46.7324, -117.0002]',
 'Moscow, US. Geo coords [41.3367, -75.5186]',
 'Moscow, US. Geo coords [41.5229, -71.7415]',
 'Moscow, US. Geo coords [35.062, -89.404]'])
    ex.setAttribute(QtCore.Qt.WA_DeleteOnClose)
    if ex.exec_() == QtWidgets.QDialog.Accepted:
        print(ex.idx)
