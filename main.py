import sys

from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QToolBar, QAction, QFileDialog, QMdiSubWindow, QTextEdit, \
    QMdiArea

from services.parse_svg import SVGParser
from ui.data_table_window import DataTableWindow


class Window(QMainWindow):
    """Main Window."""
    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)
        self.setWindowTitle("Python Menus & Toolbars")
        self.resize(1000, 500)

        self.mdi = QMdiArea()
        self.setCentralWidget(self.mdi)

        self._create_actions()
        self._createMenuBar()
        self._createToolBars()
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

    def _createToolBars(self):
        # Using a title
        fileToolBar = self.addToolBar("File")
        # Using a QToolBar object
        editToolBar = QToolBar("Edit", self)
        self.addToolBar(editToolBar)
        # Using a QToolBar object and a toolbar area
        helpToolBar = QToolBar("Help", self)
        self.addToolBar(Qt.LeftToolBarArea, helpToolBar)

    def _connect_actions(self):
        self.open_action.triggered.connect(self.open_file)
        self.save_action.triggered.connect(self.save_file)
        self.export_action.triggered.connect(self.export_table)

    def open_file(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file',
                                            str(Path.cwd()), "csv files (*.csv)")

        if fname[0] != '':
            try:
                sub = DataTableWindow(fname[0])
                self.mdi.addSubWindow(sub)
                sub.show()
                sub.showMaximized()
            except Exception as e:
                print(e)

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())