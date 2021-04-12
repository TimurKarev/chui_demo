import pandas as pd

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import QComboBox, QTableWidget, QTableWidgetItem, QHeaderView, QVBoxLayout

from models.data_model import DataModel


class ComboInOut(QComboBox):
    def __init__(self, parent, row, col, value):
        super().__init__(parent)

        self._row = row
        self._col = col
        self._parent = parent

        self._items = ['Внутренняя', 'Внешняя']

        self.addItems(self._items)
        self.setCurrentIndex(self._items.index(value))

        self.currentIndexChanged.connect(self._get_combo_value)

    def _get_combo_value(self):
        self._parent.combo_changed(self._row, self._col, self.currentText())
        return self.currentText()


class DataTableWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self._data_model = DataModel()
        self._df = self._data_model.df()
        self._table_widget = QTableWidget()

        self._table_widget.cellChanged.connect(self._cell_changed)

        self.setWindowTitle(self._data_model.filename)

        self._create_table()
        self.setWidget(self._table_widget)

    def save_model(self):
        self._df.to_csv(self._f_name, index=False, encoding='utf-8-sig')

    def _create_table(self):
        self._table_widget.setRowCount(self._df.shape[0])
        self._table_widget.setColumnCount(self._df.shape[1])

        self._table_widget.setHorizontalHeaderLabels(self._df.columns)

        header = self._table_widget.horizontalHeader()
        for r, row in self._df.iterrows():
            for c, value in enumerate(row):
                if c == 1:
                    self._table_widget.setCellWidget(r, c, ComboInOut(self, r, c, self._df.iloc[r, c]))
                else:
                    self._table_widget.setItem(r, c, QTableWidgetItem(value))
                header.setSectionResizeMode(c, QHeaderView.ResizeToContents)

    def _cell_changed(self, row, col):
        self._df.iloc[row, col] = self._table_widget.item(row, col).text()

    def combo_changed(self, row, col, value):
        self._df.iloc[row, col] = value
        print(self._df.iloc[row, col])