import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from PyQt5 import QtWidgets, Qt, QtCore
import pandas as pd
from models.data_model import DataModel
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.backends.backend_pdf


class Table(FigureCanvas):
    def __init__(self):
        table = DataModel().df

        self.fig, ax = plt.subplots(figsize=(10, 5), dpi=200)
        super().__init__(self.fig)

        cell_text = []
        for row in range(len(table)):
            cell_text.append(table.iloc[row])

        col_width = [0.03, .67, 0.1, 0.1, 0.1, 0.1, 0.1]
        ax_table = ax.table(
            colWidths=col_width,
            cellText=cell_text,
            colLabels=table.columns,
            loc='center'
        )
        ax_table.auto_set_font_size(False)
        ax_table.set_fontsize(4)
        ax.axis('off')

        # pdf = matplotlib.backends.backend_pdf.PdfPages("output.pdf")
        # pdf.savefig(fig)
        # pdf.close()


class Canvas(FigureCanvas):
    def __init__(self, parent=None, sizes=None, labels=None, title=' '):
        fig, self._ax = plt.subplots(figsize=(6, 2), dpi=200)
        self.fig = fig
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
            self._ax.set_title(title)


class GraphWindow(QtWidgets.QMainWindow):
    """Main MainWindow."""
    def __init__(self, parent):
        super().__init__(parent=parent)
        dm = DataModel()
        self.data = dm.df
        file_name = str(dm.filename)[:-3] + 'pdf'
        try:
            layout = QtWidgets.QVBoxLayout()
            pdf = PdfPages(file_name)

            table = Table()
            pdf.savefig(table.fig)
            layout.addWidget(table)

            # header1 = QtWidgets.QLabel()
            # header1.setAlignment(QtCore.Qt.AlignCenter)
            # header1.setText('<h1>Соотношение Внешних и Внутренних проблемм<h1>')
            # layout.addWidget(header1)
            df = DataModel().df.iloc[:, 2].value_counts()
            labels = df.index
            sizes = list(df)
            chart = Canvas(parent=parent,
                           labels=labels,
                           sizes=sizes,
                           title='Соотношение Внешних и Внутренних проблемм'
                           )
            layout.addWidget(chart)
            pdf.savefig(chart.fig)

            # header1 = QtWidgets.QLabel()
            # header1.setAlignment(QtCore.Qt.AlignCenter)
            # header1.setText('<h1>Структура  внутренних и внешних проблем<h1>')
            # layout.addWidget(header1)
            df = DataModel().df.iloc[:, 3].value_counts()
            labels = df.index
            sizes = list(df)
            chart = Canvas(parent=parent,
                           labels=labels,
                           sizes=sizes,
                           title='Структура  внутренних и внешних проблем'
                           )
            layout.addWidget(chart)
            pdf.savefig(chart.fig)

            # header1 = QtWidgets.QLabel()
            # header1.setAlignment(QtCore.Qt.AlignCenter)
            # header1.setText('<h1>Структура внешних проблем<h1>')
            # layout.addWidget(header1)
            mask = self.data.iloc[:, 2] == 'Внешняя'
            plot_df = self.data[mask]
            df = plot_df.iloc[:, 3].value_counts()
            labels = df.index
            sizes = list(df)
            chart = Canvas(parent=parent,
                           labels=labels,
                           sizes=sizes,
                           title='Структура внешних проблем'
                           )
            layout.addWidget(chart)
            pdf.savefig(chart.fig)

            # header1 = QtWidgets.QLabel()
            # header1.setAlignment(QtCore.Qt.AlignCenter)
            # header1.setText('<h1>Структура внутренних проблем<h1>')
            # layout.addWidget(header1)
            mask = self.data.iloc[:, 2] == 'Внутренняя'
            plot_df = self.data[mask]
            df = plot_df.iloc[:, 3].value_counts()
            labels = df.index
            sizes = list(df)
            chart = Canvas(parent=parent,
                           labels=labels,
                           sizes=sizes,
                           title='Структура внутренних проблем'
                           )
            layout.addWidget(chart)
            pdf.savefig(chart.fig)

            # header1 = QtWidgets.QLabel()
            # header1.setAlignment(QtCore.Qt.AlignCenter)
            # header1.setText('<h1>Структура бизнесс процессов<h1>')
            # layout.addWidget(header1)
            df = self.data.iloc[:, 4].value_counts()
            labels = df.index
            sizes = list(df)
            chart = Canvas(parent=parent,
                           labels=labels,
                           sizes=sizes,
                           title='Структура бизнесс процессов'
                           )
            layout.addWidget(chart)
            pdf.savefig(chart.fig)

            # header1 = QtWidgets.QLabel()
            # header1.setAlignment(QtCore.Qt.AlignCenter)
            # header1.setText('<h1>Структура типов бизнесс процессов<h1>')
            # layout.addWidget(header1)
            df = self.data.iloc[:, 5].value_counts()
            labels = df.index
            sizes = list(df)
            chart = Canvas(parent=parent,
                           labels=labels,
                           sizes=sizes,
                           title='Структура типов бизнесс процессов'
                           )
            layout.addWidget(chart)
            pdf.savefig(chart.fig)

            # header1 = QtWidgets.QLabel()
            # header1.setAlignment(QtCore.Qt.AlignCenter)
            # header1.setText('<h1>Распределение задач по ЗГД<h1>')
            # layout.addWidget(header1)
            df = self.data.iloc[:, 6].value_counts()
            labels = df.index
            sizes = list(df)
            chart = Canvas(parent=parent,
                           labels=labels,
                           sizes=sizes,
                           title='Структура типов бизнесс процессов'
                           )
            layout.addWidget(chart)
            pdf.savefig(chart.fig)

            pdf.close()

            layout.addStretch()

            widget = QtWidgets.QWidget()
            widget.setLayout(layout)
            scroll = QtWidgets.QScrollArea()
            scroll.setAlignment(QtCore.Qt.AlignCenter)
            scroll.setWidget(widget)
            self.setCentralWidget(scroll)
        except Exception as e:
            print(f'graph window __init__ {e}')

