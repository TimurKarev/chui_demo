from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QComboBox, QTableWidgetItem, QHeaderView

from models.data_model import DataModel


class ComboInOut(QComboBox):
    def __init__(self, parent, row, col, value):
        super().__init__(parent)

        self._row = row
        self._col = col
        self._parent = parent

        self._items = ['Внутренняя', 'Внешняя']
        if value == '' or value == ' ':
            value = self._items[0]
            self._get_combo_value()

        self.addItems(self._items)
        self.setCurrentIndex(self._items.index(value))

        self.currentIndexChanged.connect(self._get_combo_value)

    def _get_combo_value(self):
        self._parent.combo_changed(self._row, self._col, self.currentText())
        return self.currentText()


class TableWidget(QtWidgets.QTableWidget):
    def __init__(self, parent):
        super().__init__()
        self._parent = parent
        self._data_model = DataModel()
        self._df = self._data_model.df

        self.cellChanged.connect(self._cell_changed)

        self.create_table()
        try:
            self.setContextMenuPolicy(Qt.CustomContextMenu)
            self.customContextMenuRequested.connect(self.generateMenu)
        except Exception as e:
            print(e)

    def create_table(self):
        self._df = self._data_model.df

        self.setRowCount(self._df.shape[0])
        self.setColumnCount(self._df.shape[1])

        self.setHorizontalHeaderLabels(self._df.columns)

        header = self.horizontalHeader()
        for r, row in self._df.iterrows():
            for c, value in enumerate(row):
                if c == 1:
                    self.setCellWidget(r, c, ComboInOut(self, r, c, self._df.iloc[r, c]))
                else:
                    self.setItem(r, c, QTableWidgetItem(value))
                header.setSectionResizeMode(c, QHeaderView.ResizeToContents)

    # pos is the clicked position
    def generateMenu(self):
        row_num = -1
        for i in self.selectionModel().selection().indexes():
            row_num = i.row()
        if row_num != -1:
            try:
                dm = DataModel()
                dm.delete_row(row_num)
                self.create_table()
                self.update()
            except Exception as e:
                print(e)

    def _cell_changed(self, row, col):
        self._df.iloc[row, col] = self.item(row, col).text()

    def combo_changed(self, row, col, value):
        self._df.iloc[row, col] = value
