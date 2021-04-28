import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from PyQt5 import QtWidgets, Qt, QtCore
from models.data_model import DataModel
from matplotlib.backends.backend_pdf import PdfPages


class Table(FigureCanvas):
    x_figsize = 10
    y_figsize_mult = 0.2

    def __init__(self, table, title=' '):
        y_figsize = int(self.y_figsize_mult * table.shape[0]) + 1
        self.fig, ax = plt.subplots(figsize=(self.x_figsize, y_figsize), dpi=200, constrained_layout=True)
        super().__init__(self.fig)
        self.fig.suptitle(title, fontsize=10)
        cell_text = []
        for row in range(len(table)):
            cell_text.append(table.iloc[row])

        col_width = [0.03, .57, 0.1, 0.2, 0.1, 0.1, 0.1]

        ax_table = ax.table(
            colWidths=col_width,
            cellText=cell_text,
            colLabels=table.columns,
            loc='center'
        )

        ax_table.auto_set_font_size(False)
        ax_table.set_fontsize(4)
        ax.axis('off')


class SimplePieCanvas(FigureCanvas):
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


class MultiPieCanvas(FigureCanvas):
    x_figsize_mult = 5
    y_figsize_mult = 3
    x_count = 2

    def __init__(self, parent=None, data=None, title=' '):
        x = self.x_count * self.x_figsize_mult
        y_count = len(data) // self.x_count + 1
        y = y_count * self.y_figsize_mult
        fig = plt.figure(figsize=(x, y), dpi=200, constrained_layout=True)
        font = {'size': 6}

        plt.rc('font', **font)
        fig.suptitle(title, fontsize=10)
        super().__init__(fig)
        if parent:
            self.setParent(parent)

        for i, value in enumerate(data):
            ax = fig.add_subplot(y_count, self.x_count, i + 1)
            sizes = value['sizes']
            labels = value['labels']
            ax_title = value['title']
            if sizes:
                size_len = len(sizes)
                explode = [0] * size_len
                if size_len > 2:
                    e = sizes.index(max(sizes))
                    explode[int(e)] = 0.1

                ax.pie(sizes,
                       labels=labels,
                       explode=explode,
                       autopct='%1.1f%%',
                       radius=1,
                       wedgeprops=dict(width=0.9,
                                       edgecolor='w',
                                       ),
                       )
                ax.set_title(ax_title)
        self.fig = fig


class GraphWindow(QtWidgets.QMainWindow):
    """Main MainWindow."""

    def __init__(self, parent):
        super().__init__(parent=parent)
        dm = DataModel()
        data = dm.df
        file_name = str(dm.filename)[:-3] + 'pdf'
        try:
            layout = QtWidgets.QVBoxLayout()
            pdf = PdfPages(file_name)

            table = Table(data, title='Общая таблица проблем')
            pdf.savefig(table.fig)
            layout.addWidget(table)

            zgd_list = data['З.Г.Д.'].unique()
            table_data = data[data['З.Г.Д.'] == zgd_list[0]]
            table = Table(table=table_data, title=zgd_list[0])
            pdf.savefig(table.fig)
            layout.addWidget(table)

            df = data.iloc[:, 2].value_counts()
            pie_dict = {
                'labels': df.index,
                'sizes': list(df),
                'title': 'Соотношение Внешних и Внутренних проблемм'
            }
            pie_data = [pie_dict]

            df = data.iloc[:, 3].value_counts()
            pie_dict = {
                'labels': df.index,
                'sizes': list(df),
                'title': 'Структура  внутренних и внешних проблем'
            }
            pie_data.append(pie_dict)

            mask = data.iloc[:, 2] == 'Внешняя'
            plot_df = data[mask]
            df = plot_df.iloc[:, 3].value_counts()
            pie_dict = {
                'labels': df.index,
                'sizes': list(df),
                'title': 'Структура внешних проблем'
            }
            pie_data.append(pie_dict)

            mask = data.iloc[:, 2] == 'Внутренняя'
            plot_df = data[mask]
            df = plot_df.iloc[:, 3].value_counts()
            pie_dict = {
                'labels': df.index,
                'sizes': list(df),
                'title': 'Структура внутренних проблем'
            }
            pie_data.append(pie_dict)

            df = data.iloc[:, 4].value_counts()
            pie_dict = {
                'labels': df.index,
                'sizes': list(df),
                'title': 'Структура бизнес процессов'
            }
            pie_data.append(pie_dict)

            df = data.iloc[:, 5].value_counts()
            pie_dict = {
                'labels': df.index,
                'sizes': list(df),
                'title': 'Структура типов бизнесс процессов'
            }
            pie_data.append(pie_dict)

            df = data.iloc[:, 6].value_counts()
            pie_dict = {
                'labels': df.index,
                'sizes': list(df),
                'title': 'Распределение задач по ЗГД'
            }
            pie_data.append(pie_dict)

            chart = MultiPieCanvas(parent=parent, data=pie_data, title='Общий расклад')
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
