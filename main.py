import sys

from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QToolBar, QAction, QFileDialog, QMdiSubWindow, QTextEdit, \
    QMdiArea

from ui.data_table_window import DataTableWindow


class Window(QMainWindow):
    """Main Window."""
    def __init__(self, parent=None):
        """Initializer."""
        super().__init__(parent)
        self.setWindowTitle("Python Menus & Toolbars")
        self.resize(400, 200)
        self.mdi = QMdiArea()
        self.setCentralWidget(self.mdi)

        self._create_actions()
        self._createMenuBar()
        self._createToolBars()
        self._connect_actions()


    def _create_actions(self):
        self.open_action = QAction("&Open...", self)

    def _createMenuBar(self):
        menuBar = self.menuBar()
        self.setMenuBar(menuBar)
        fileMenu =menuBar.addMenu("&Файл")
        fileMenu.addAction(self.open_action)

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

    def open_file(self):
        # fname = QFileDialog.getOpenFileName(self, 'Open file',
        #                                     str(Path.cwd()), "csv files (*.csv)")
        # print(fname)
        # if fname[0] != '':
        #     self.centralWidget.setText(fname[0])
        sub = QMdiSubWindow()
        sub.setWidget(DataTableWindow())
        sub.setWindowTitle("subwindow")
        self.mdi.addSubWindow(sub)
        sub.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())