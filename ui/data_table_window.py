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
        if value == '':
            value = self._items[0]

        self.addItems(self._items)
        self.setCurrentIndex(self._items.index(value))

        self.currentIndexChanged.connect(self._get_combo_value)

    def _get_combo_value(self):
        self._parent.combo_changed(self._row, self._col, self.currentText())
        return self.currentText()


class TableWidget(QtWidgets.QTableWidget):
    def __init__(self):
        super().__init__()
        self._data_model = DataModel()
        self._df = self._data_model.df

        self.cellChanged.connect(self._cell_changed)

        self.create_table()

    # def save_model(self):
    #     self._df.to_csv(self._f_name, index=False, encoding='utf-8-sig')

    def _generate_menu(self):
        print('click')

    def create_table(self):
        self.setRowCount(self._df.shape[0])#if self._df.shape[0] > 0 else 1)
        self.setColumnCount(self._df.shape[1])
        print(f'create table {self._df.shape}')
        self.setHorizontalHeaderLabels(self._df.columns)

        header = self.horizontalHeader()
        for r, row in self._df.iterrows():
            for c, value in enumerate(row):
                if c == 1:
                    self.setCellWidget(r, c, ComboInOut(self, r, c, self._df.iloc[r, c]))
                else:
                    self.setItem(r, c, QTableWidgetItem(value))
                header.setSectionResizeMode(c, QHeaderView.ResizeToContents)

    def _cell_changed(self, row, col):
        self._df.iloc[row, col] = self.item(row, col).text()

    def combo_changed(self, row, col, value):
        self._df.iloc[row, col] = value
