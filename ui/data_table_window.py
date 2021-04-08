import pandas as pd

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import QComboBox, QTableWidget, QTableWidgetItem, QHeaderView, QVBoxLayout


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


class Delegate(QtWidgets.QItemDelegate):
    def __init__(self, owner):
        super().__init__(owner)

    def createEditor(self, parent, option, index):
        editor = ComboInOut(parent)
        #editor.currentItemChanged.connect(self.currentItemChanged)
        editor.addItems(self.items)
        return editor


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


class DataTableWindow(QtWidgets.QMdiSubWindow):
    def __init__(self, f_name):
        super().__init__()
        self._df = pd.DataFrame()
        self._table_widget = QTableWidget()

        self._table_widget.cellChanged.connect(self._cell_changed)

        self.setWindowTitle(f_name)

        self._init_model(f_name)
        self._create_table()
        self.setWidget(self._table_widget)

    def _init_model(self, f_name):
        self._df = pd.read_csv(f_name)

    def _create_table(self):
        # Row count
        self._table_widget.setRowCount(self._df.shape[0])

        # Column count
        self._table_widget.setColumnCount(self._df.shape[1])

        for r, row in self._df.iterrows():
            for c, value in enumerate(row):
                if c == 1:
                    self._table_widget.setCellWidget(r, c, ComboInOut(self, r, c, self._df.iloc[r, c]))
                self._table_widget.setItem(r, c, QTableWidgetItem(value))

        # Table will fit the screen horizontally
        self._table_widget.horizontalHeader().setStretchLastSection(True)
        self._table_widget.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)

    def _cell_changed(self, row, col):
        self._df.iloc[row, col] = self._table_widget.item(row, col).text()

    def combo_changed(self, row, col, value):
        self._df.iloc[row, col] = value
        print(self._df.iloc[row, col])