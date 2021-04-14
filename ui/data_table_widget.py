from PyQt5 import QtWidgets, QtCore, Qt

from models.data_model import DataModel
from ui.data_table_window import TableWidget


class DataTableWidget(QtWidgets.QTabWidget):
    def __init__(self):
        super().__init__()
        self._layout = QtWidgets.QVBoxLayout()
        self._create_window()

    def _create_window(self):
        t1_header = QtWidgets.QLabel()
        t1_header.setAlignment(QtCore.Qt.AlignCenter)
        t1_header.setText('<h3>Таблица потерь - Проблеммы<h3>')
        self._layout.addWidget(t1_header)

        table = TableWidget()
        table.setSizePolicy(Qt.QSizePolicy.Expanding, Qt.QSizePolicy.Expanding)
        self._layout.addWidget(table)
        self._table = table

        add_button = QtWidgets.QPushButton('Добавить строку')
        add_button.clicked.connect(self._add_button_clicked)
        self._layout.addWidget(add_button)

        self._layout.addStretch()

        file_name_label = QtWidgets.QLabel()
        file_name_label.setText(str(DataModel().filename))
        self._layout.addWidget(file_name_label)

        #layout.addStretch()
        self.setLayout(self._layout)

    def _add_button_clicked(self):
        try:
            DataModel().add_empty_row()
            self._table.create_table()
            self.update()
        except Exception as e:
            print(e)
