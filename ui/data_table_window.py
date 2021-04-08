import pandas as pd

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QComboBox


class ComboInOut(QComboBox):
    def __init__(self, parent):
        super().__init__(parent)
        self.addItems(['Внутрення', 'Внешняя'])
        self.currentIndexChanged.connect(self._get_combo_value)

    def _get_combo_value(self):
        return self.currentText()


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def setData(self, index, value, role):
        if role == Qt.EditRole:
            self._data.iloc[index.row(), index.column()] = value
            return True

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def flags(self, index):
        return Qt.ItemIsSelectable|Qt.ItemIsEnabled|Qt.ItemIsEditable

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

        data = pd.read_csv(fname)

        self.model = TableModel(data)
        self.table.setModel(self.model)
        self.table.resizeColumnsToContents()
        #self.table.setCellWidget(0, 1, ComboInOut(self))
        self.setCentralWidget(self.table)
