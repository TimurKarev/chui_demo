import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from PyQt5 import QtWidgets, Qt, QtCore
import pandas as pd
from models.data_model import DataModel
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.backends.backend_pdf

class Table(FigureCanvas):
    def __init__(self):
        d = DataModel().df

        table = pd.DataFrame(d)
        self.fig, ax = plt.subplots(figsize=(10, 5), dpi=200)
        super().__init__(self.fig)

        cell_text = []
        for row in range(len(table)):
            cell_text.append(table.iloc[row])

        col_width = [.5, 0.1, 0.1, 0.1, 0.1, 0.1]
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
    def __init__(self, parent=None, sizes=None, labels=None):
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


class GraphWindow(QtWidgets.QMainWindow):
    """Main MainWindow."""
    def __init__(self, parent):
        super().__init__(parent=parent)
        self.data = DataModel().df
        try:
            layout = QtWidgets.QVBoxLayout()
            pdf = PdfPages('1.pdf')

            table = Table()
            pdf.savefig(table.fig)
            layout.addWidget(table)

            header1 = QtWidgets.QLabel()
            header1.setAlignment(QtCore.Qt.AlignCenter)
            header1.setText('<h1>Соотношение Внешних и Внутренних проблемм<h1>')
            layout.addWidget(header1)
            df = DataModel().df.iloc[:, 1].value_counts()
            labels = df.index
            sizes = list(df)
            chart = Canvas(parent=parent,
                           labels=labels,
                           sizes=sizes)
            layout.addWidget(chart)
            pdf.savefig(chart.fig)

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
            pdf.savefig(chart.fig)

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
            pdf.savefig(chart.fig)

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
            pdf.savefig(chart.fig)

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
            pdf.savefig(chart.fig)

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
            pdf.savefig(chart.fig)

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
            print(e)

