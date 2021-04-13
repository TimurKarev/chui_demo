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
        self._table = table

        add_button = QtWidgets.QPushButton('Добавить строку')
        add_button.clicked.connect(self._add_button_clicked)
        layout.addWidget(add_button)

        layout.addStretch()

        file_name_label = QtWidgets.QLabel()
        file_name_label.setText(str(DataModel().filename))
        layout.addWidget(file_name_label)

        #layout.addStretch()
        self.setLayout(layout)

    def _add_button_clicked(self):
        print("but clicked")
        DataModel().add_empty_row()
        self._table.create_table()
        self._table.update()
