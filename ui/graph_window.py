import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from PyQt5 import QtWidgets, Qt, QtCore

from models.data_model import DataModel


class Canvas(FigureCanvas):
    def __init__(self, parent=None, sizes=None, labels=None):
        fig, self._ax = plt.subplots(figsize=(6, 2), dpi=200)
        font = {'size': 6}

        plt.rc('font', **font)
        super().__init__(fig)
        if parent:
            self.setParent(parent)

        if sizes:
            size_len = len(sizes)
            explode = [0] * size_len
            if size_len > 2:
                e = sizes.index(max(sizes))
                explode[int(e)] = 0.1

            self._ax.pie(sizes,
                         labels=labels,
                         explode=explode,
                         autopct='%1.1f%%',
                         radius=1,
                         wedgeprops=dict(width=0.9,
                                         edgecolor='w',
                                         ),
                         )


class GraphWindow(QtWidgets.QMainWindow):
    """Main MainWindow."""
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.data = DataModel().df
        try:
            layout = QtWidgets.QVBoxLayout()

            header1 = QtWidgets.QLabel()
            header1.setAlignment(QtCore.Qt.AlignCenter)
            header1.setText('<h1>Соотношение Внешних и Внутренних проблемм<h1>')
            layout.addWidget(header1)
            df = DataModel().df.iloc[:, 1].value_counts()
            labels = df.index
            sizes = list(df)
            print(f'sizes {sizes} \n labels {labels}')
            chart = Canvas(parent=parent,
                           labels=labels,
                           sizes=sizes)
            layout.addWidget(chart)

            header1 = QtWidgets.QLabel()
            header1.setAlignment(QtCore.Qt.AlignCenter)
            header1.setText('<h1>Структура  внутренних и внешних проблем<h1>')
            layout.addWidget(header1)
            df = DataModel().df.iloc[:, 2].value_counts()
            labels = df.index
            sizes = list(df)
            chart = Canvas(parent=parent,
                           labels=labels,
                           sizes=sizes)
            layout.addWidget(chart)

            header1 = QtWidgets.QLabel()
            header1.setAlignment(QtCore.Qt.AlignCenter)
            header1.setText('<h1>Структура внешних проблем<h1>')
            layout.addWidget(header1)
            mask = self.data.iloc[:, 1] == 'Внешняя'
            plot_df = self.data[mask]
            df = plot_df.iloc[:, 2].value_counts()
            labels = df.index
            sizes = list(df)

            chart = Canvas(parent=parent,
                           labels=labels,
                           sizes=sizes)
            layout.addWidget(chart)

            header1 = QtWidgets.QLabel()
            header1.setAlignment(QtCore.Qt.AlignCenter)
            header1.setText('<h1>Структура внутренних проблем<h1>')
            layout.addWidget(header1)
            mask = self.data.iloc[:, 1] == 'Внутренняя'
            plot_df = self.data[mask]
            df = plot_df.iloc[:, 2].value_counts()
            labels = df.index
            sizes = list(df)
            chart = Canvas(parent=parent,
                           labels=labels,
                           sizes=sizes)
            layout.addWidget(chart)

            header1 = QtWidgets.QLabel()
            header1.setAlignment(QtCore.Qt.AlignCenter)
            header1.setText('<h1>Структура бизнесс процессов<h1>')
            layout.addWidget(header1)
            df = self.data.iloc[:, 3].value_counts()
            labels = df.index
            sizes = list(df)

            chart = Canvas(parent=parent,
                           labels=labels,
                           sizes=sizes)
            layout.addWidget(chart)

            header1 = QtWidgets.QLabel()
            header1.setAlignment(QtCore.Qt.AlignCenter)
            header1.setText('<h1>Структура типов бизнесс процессов<h1>')
            layout.addWidget(header1)
            df = self.data.iloc[:, 4].value_counts()
            labels = df.index
            sizes = list(df)
            chart = Canvas(parent=parent,
                           labels=labels,
                           sizes=sizes)
            layout.addWidget(chart)

            header1 = QtWidgets.QLabel()
            header1.setAlignment(QtCore.Qt.AlignCenter)
            header1.setText('<h1>Распределение задач по ЗГД<h1>')
            layout.addWidget(header1)
            df = self.data.iloc[:, 5].value_counts()
            labels = df.index
            sizes = list(df)
            chart = Canvas(parent=parent,
                           labels=labels,
                           sizes=sizes)
            layout.addWidget(chart)

            layout.addStretch()

            widget = QtWidgets.QWidget()
            widget.setLayout(layout)
            scroll = QtWidgets.QScrollArea()
            scroll.setAlignment(QtCore.Qt.AlignCenter)
            scroll.setWidget(widget)
            self.setCentralWidget(scroll)
        except Exception as e:
            print(e)
