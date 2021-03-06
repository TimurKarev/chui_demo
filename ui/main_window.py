import sys

from pathlib import Path

from models.data_model import DataModel
from ui.data_table_widget import DataTableWidget
from PyQt5 import QtCore

from PyQt5.QtWidgets import QMainWindow, QToolBar, QAction, QFileDialog, \
    QMdiArea, QLabel
from ui.graph_window import GraphWindow
import pdfkit


class MainWindow(QMainWindow):
    """Main MainWindow."""
    def __init__(self, app):
        """Initializer."""
        super().__init__(None)
        self._app = app
        self.setWindowTitle("Python Menus & Toolbars")
        self.resize(1000, 500)

        self.mdi = QMdiArea()
        self.setCentralWidget(self.mdi)

        self._create_actions()
        self._createMenuBar()
        self._connect_actions()

    def _createMenuBar(self):
        menuBar = self.menuBar()
        self.setMenuBar(menuBar)

        fileMenu =menuBar.addMenu("&Файл")
        fileMenu.addAction(self.new_action)
        fileMenu.addAction(self.open_action)
        fileMenu.addSeparator()
        fileMenu.addAction(self.import_action)
        fileMenu.addAction(self.export_action)
        fileMenu.addSeparator()
        fileMenu.addAction(self.save_action)
        fileMenu.addAction(self.save_as_action)
        fileMenu.addSeparator()
        fileMenu.addAction(self.close_table_action)
        fileMenu.addAction(self.exit_action)

        graph_menu = menuBar.addMenu("График")
        graph_menu.addAction(self.show_graph_action)

    def _create_actions(self):
        self.new_action = QAction("&Новая таблица", self)
        self.open_action = QAction("&Открыть...", self)
        self.import_action = QAction("&Импорт из svg", self)
        self.export_action = QAction("&Экспорт в pdf", self)
        self.save_action = QAction("&Сохранить", self)
        self.save_as_action = QAction('Сохранить как...', self)
        self.close_table_action = QAction('Закрыть таблицу', self)
        self.exit_action = QAction('Выйти', self)

        self.show_graph_action = QAction('Нарисовать график', self)

    def _connect_actions(self):
        self.new_action.triggered.connect(self.new_table)
        self.open_action.triggered.connect(self.open_file)
        self.import_action.triggered.connect(self.import_table)
        self.export_action.triggered.connect(self.export_to_pdf)
        self.save_action.triggered.connect(self.save_file)
        self.save_as_action.triggered.connect(self.save_as_file)
        self.close_table_action.triggered.connect(self.close_table)
        self.exit_action.triggered.connect(self.exit)

        self.show_graph_action.triggered.connect(self.show_graph)

    def new_table(self):
        try:
            DataModel().new_table()
            window = DataTableWidget()
            self.setCentralWidget(window)
        except Exception as e:
            print(e)

    def open_file(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file',
                                            str(Path.cwd()), "csv files (*.csv)")

        if fname[0] != '':
            try:
                DataModel().load_from_csv(fname[0])
                window = DataTableWidget()
                self.setCentralWidget(window)
            except Exception as e:
                print('main window open file' + e)

    def save_file(self):
        try:
            dm = DataModel()
            dm.df.to_csv(dm.filename, index=False, encoding='utf-8-sig')
        except Exception as e:
            print('main window save as' + e)

    def save_as_file(self):
        fname = QFileDialog.getSaveFileName(self, 'Сохранить как',
                                            str(Path.cwd()), "csv files (*.csv)")
        if fname[0] != '':
            try:
                dm = DataModel()
                dm.filename = fname[0]
                dm.df.to_csv(dm.filename, index=False, encoding='utf-8-sig')
                dm.filename = fname
            except Exception as e:
                print('main window save as' + e)

    def import_table(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file',
                                            str(Path.cwd()), "svg files (*.svg)")
        try:
            dm = DataModel()
            dm.load_from_svg(fname[0])
            window = DataTableWidget()
            self.setCentralWidget(window)
        except Exception as e:
            print(e)

    def export_to_pdf(self):
        # dm = DataModel()
        # html_content = dm.get_html_from_df()
        # try:
        #     pdfkit.from_string(html_content, 'out.pdf')
        # except Exception as e:
        #     print(e)
        pass

    def close_table(self):
        empty_label = QLabel()
        empty_label.setText('загрузите таблицу')
        empty_label.setAlignment(QtCore.Qt.AlignCenter)
        self.setCentralWidget(empty_label)

    def exit(self):
        sys.exit(self._app.exec_())

    def show_graph(self):
        GraphWindow(self).show()