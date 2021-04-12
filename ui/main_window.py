from pathlib import Path

from models.data_model import DataModel
from services.parse_svg import SVGParser
from ui.data_table_widget import DataTableWidget
from ui.data_table_window import DataTableWidget
from PyQt5 import QtWidgets

from PyQt5.QtWidgets import QMainWindow, QToolBar, QAction, QFileDialog, \
    QMdiArea, QLabel

from PyQt5 import Qt


class MainWindow(QMainWindow):
    """Main MainWindow."""
    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)
        self.setWindowTitle("Python Menus & Toolbars")
        self.resize(1000, 500)

        self.mdi = QMdiArea()
        self.setCentralWidget(self.mdi)

        self._create_actions()
        self._createMenuBar()
        self._connect_actions()


    def _create_actions(self):
        self.open_action = QAction("&Открыть...", self)
        self.save_action = QAction("&Сохранить", self)
        self.export_action = QAction("&Экспорт из SVG", self)

    def _createMenuBar(self):
        menuBar = self.menuBar()
        self.setMenuBar(menuBar)

        fileMenu =menuBar.addMenu("&Файл")
        fileMenu.addAction(self.open_action)
        fileMenu.addAction(self.save_action)
        fileMenu.addAction(self.export_action)

    def _connect_actions(self):
        self.open_action.triggered.connect(self.open_file)
        self.save_action.triggered.connect(self.save_file)
        self.export_action.triggered.connect(self.export_table)

    def open_file(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file',
                                            str(Path.cwd()), "csv files (*.csv)")

        if fname[0] != '':
            try:
                DataModel().load_from_csv(fname[0])
                window = DataTableWidget()
                self.setCentralWidget(window)
            except Exception as e:
                print('main window' + e)

    def save_file(self):
        window = self.mdi.activeSubWindow()
        if window != 0:
            try:
                window.save_model()
            except Exception as e:
                # TODO: create good exception
                print('Can not save file')

    def export_table(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file',
                                            str(Path.cwd()), "svg files (*.svg)")
        try:
            l = SVGParser.parse_svg(fname[0])
            print(l)
        except Exception as e:
            print(e)