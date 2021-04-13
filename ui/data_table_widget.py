from PyQt5 import QtWidgets, QtCore, Qt

from models.data_model import DataModel
from ui.data_table_window import TableWidget


class DataTableWidget(QtWidgets.QTabWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout()

        t1_header = QtWidgets.QLabel()
        t1_header.setAlignment(QtCore.Qt.AlignCenter)
        t1_header.setText('<h3>Таблица потерь - Проблеммы<h3>')
        layout.addWidget(t1_header)

        table = TableWidget()
        table.setSizePolicy(Qt.QSizePolicy.Expanding, Qt.QSizePolicy.Expanding)
        layout.addWidget(table)

        file_name_label = QtWidgets.QLabel()
        file_name_label.setText(str(DataModel().filename))
        layout.addWidget(file_name_label)

        #layout.addStretch()
        self.setLayout(layout)
