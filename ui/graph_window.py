import numpy
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from PyQt5.QtWidgets import QMainWindow


class Canvas(FigureCanvas):
    def __init__(self, parent):
        fig, self._ax = plt.subplots(figsize=(5,4), dpi=200)
        super().__init__(fig)
        self.setParent(parent)

        t = np.arange(0.0, 2.0, 0.01)
        s = 1 + np.sin(2 * np.pi * t)

        self._ax.plot(t, s)
        self._ax.grid()


class GraphWindow(QMainWindow):
    """Main MainWindow."""
    def __init__(self, parent):
        super().__init__(parent=parent)
        chart = Canvas(self)
