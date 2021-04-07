import sys
import pandas as pd

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    # def setData(self, index, value, role):
    #     if role == Qt.EditRole:
    #         self._data[index.row()][index.column()] = value
    #         print(self._data)
    #         return True

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    # def flags(self, index):
    #     return Qt.ItemIsSelectable|Qt.ItemIsEnabled|Qt.ItemIsEditable

    def headerData(self, section, orientation, role):
        # section is the index of the column/row.
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Vertical:
                return str(self._data.index[section])

class DataTableWindow(QtWidgets.QMainWindow):
    def __init__(self, fname):
        super().__init__()

        self.table = QtWidgets.QTableView()

        # data = [
        #   [4, 9, 2],
        #   [1, 0, 0],
        #   [3, 5, 0],
        #   [3, 3, 2],
        #   [7, 8, 9],
        # ]

        data = pd.read_csv(fname)

        self.model = TableModel(data)
        self.table.setModel(self.model)

        self.setCentralWidget(self.table)