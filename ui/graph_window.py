import numpy
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from PyQt5 import QtWidgets, Qt, QtCore

from models.data_model import DataModel


class Canvas(FigureCanvas):
    def __init__(self, parent):
        fig, self._ax = plt.subplots(figsize=(3, 2), dpi=200)
        super().__init__(fig)
        self.setParent(parent)

        df = DataModel().df.iloc[:, 1].value_counts()

        labels = df.index
        sizes = list(df)

        size_len = len(sizes)
        explode = [0] * size_len
        if size_len > 2:
            e = sizes.index(max(sizes))
            explode[int(e)] = 0.05

        self._ax.pie(sizes,
                     labels=labels,
                     explode=explode,
                     autopct='%1.1f%%',
                     radius=1,
                     wedgeprops=dict(width=0.6,
                                     edgecolor='w',
                                     ),
                     )


class GraphWindow(QtWidgets.QMainWindow):
    """Main MainWindow."""
    def __init__(self, parent):
        super().__init__(parent=parent)
        try:
            layout = QtWidgets.QVBoxLayout()

            header1 = QtWidgets.QLabel()
            header1.setAlignment(QtCore.Qt.AlignCenter)
            header1.setText('<h1>Внешняя Внутреняя<h1>')
            layout.addWidget(header1)

            chart = Canvas(self)
            layout.addWidget(chart)

            layout.addStretch()

            widget = QtWidgets.QWidget()
            widget.setLayout(layout)
            self.setCentralWidget(widget)
        except Exception as e:
            print(e)
