from PyQt5 import QtWidgets, QtCore


class DataTableWidget(QtWidgets.QTabWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout()

        t1_header = QtWidgets.QLabel()
        t1_header.setAlignment(QtCore.Qt.AlignCenter)
        t1_header.setText('<h3>Таблица потерь - Проблеммы<h3>')
        layout.addWidget(t1_header)

        layout.addWidget(DataTableWidget())
        layout.addWidget(QtWidgets.QPushButton("Bottom"))

        layout.addStretch()
        self.setLayout(layout)
