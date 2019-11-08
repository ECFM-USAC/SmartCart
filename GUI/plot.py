from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton, QGroupBox
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque, defaultdict
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import statistics as stats
import numpy as np
plt.style.use('seaborn')

class Canvas(FigureCanvas):
    def __init__(self, parent=None, width=6, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.compute_initial_figure()
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        #self.axes.plot([0, 1, 2, 3], [1, 2, 0, 4], 'r')
        pass

class DataPlot:
    def __init__(self, max_entries=50):
        self.axis_t = deque(maxlen=max_entries)
        self.axis_x = deque(maxlen=max_entries)
        self.axis_y1 = deque(maxlen=max_entries)
        self.axis_y2 = deque(maxlen=max_entries)
        self.axis_y3 = deque(maxlen=max_entries)
        self.axis_y4 = deque(maxlen=max_entries)
        self.axis_y5 = deque(maxlen=max_entries)
        self.axis_y6 = deque(maxlen=max_entries)
        self.axis_y7 = deque(maxlen=max_entries)
        self.axis_y8 = deque(maxlen=max_entries)
        self.axis_y9 = deque(maxlen=max_entries)
        self.axis_y10 = deque(maxlen=max_entries)
        self.axis_y11 = deque(maxlen=max_entries)
        self.axis_y12 = deque(maxlen=max_entries)
        self.max_entries = max_entries
        self.buf = deque(maxlen=25)
        self.Vmed = [0,0,0,0,0,0,0,0,0,0,0,0]
        self.Vmax = [0,0,0,0,0,0,0,0,0,0,0,0]
        self.Vmin = [0,0,0,0,0,0,0,0,0,0,0,0]

    def act(self, max_entries):
        self.axis_t = deque(maxlen=max_entries)
        self.axis_x = deque(maxlen=max_entries)
        self.axis_y1 = deque(maxlen=max_entries)
        self.axis_y2 = deque(maxlen=max_entries)
        self.axis_y3 = deque(maxlen=max_entries)
        self.axis_y4 = deque(maxlen=max_entries)
        self.axis_y5 = deque(maxlen=max_entries)
        self.axis_y6 = deque(maxlen=max_entries)
        self.axis_y7 = deque(maxlen=max_entries)
        self.axis_y8 = deque(maxlen=max_entries)
        self.axis_y9 = deque(maxlen=max_entries)
        self.axis_y10 = deque(maxlen=max_entries)
        self.axis_y11 = deque(maxlen=max_entries)
        self.axis_y12 = deque(maxlen=max_entries)
        self.max_entries = max_entries
        self.buf = deque(maxlen=25)
        print("Data actualizada")

    def add(self, x, y):
        self.axis_x.append(x)
        self.axis_y = y
        self.axis_y1.append(y[0])
        self.axis_y2.append(y[1])
        self.axis_y3.append(y[2])
        self.axis_y4.append(y[3])
        self.axis_y5.append(y[4])
        self.axis_y6.append(y[5])
        self.axis_y7.append(y[6])
        self.axis_y8.append(y[7])
        self.axis_y9.append(y[8])
        self.axis_y10.append(y[9])
        self.axis_y11.append(y[10])
        self.axis_y12.append(y[11])
        self.axis_t.append(y[12])
        self.Vmed[0] = stats.mean(self.axis_y1)
        self.Vmed[1] = stats.mean(self.axis_y2)
        self.Vmed[2] = stats.mean(self.axis_y3)
        self.Vmed[3] = stats.mean(self.axis_y4)
        self.Vmed[4] = stats.mean(self.axis_y5)
        self.Vmed[5] = stats.mean(self.axis_y6)
        self.Vmed[6] = stats.mean(self.axis_y7)
        self.Vmed[7] = stats.mean(self.axis_y8)
        self.Vmed[8] = stats.mean(self.axis_y9)
        self.Vmed[9] = stats.mean(self.axis_y10)
        self.Vmed[10] = stats.mean(self.axis_y11)
        self.Vmed[11] = stats.mean(self.axis_y12)
        self.Vmax[0] = max(self.axis_y1)
        self.Vmax[1] = max(self.axis_y2)
        self.Vmax[2] = max(self.axis_y3)
        self.Vmax[3] = max(self.axis_y4)
        self.Vmax[4] = max(self.axis_y5)
        self.Vmax[5] = max(self.axis_y6)
        self.Vmax[6] = max(self.axis_y7)
        self.Vmax[7] = max(self.axis_y8)
        self.Vmax[8] = max(self.axis_y9)
        self.Vmax[9] = max(self.axis_y10)
        self.Vmax[10] = max(self.axis_y11)
        self.Vmax[11] = max(self.axis_y12)
        self.Vmin[0] = min(self.axis_y1)
        self.Vmin[1] = min(self.axis_y2)
        self.Vmin[2] = min(self.axis_y3)
        self.Vmin[3] = min(self.axis_y4)
        self.Vmin[4] = min(self.axis_y5)
        self.Vmin[5] = min(self.axis_y6)
        self.Vmin[6] = min(self.axis_y7)
        self.Vmin[7] = min(self.axis_y8)
        self.Vmin[8] = min(self.axis_y9)
        self.Vmin[9] = min(self.axis_y10)
        self.Vmin[10] = min(self.axis_y11)
        self.Vmin[11] = min(self.axis_y12)

class RealTimePlot(Canvas):
    def __init__(self, *args, **kwargs):
        Canvas.__init__(self, *args, **kwargs)

    def update_figure(self, data, state, stateN, graph):
        self.axes.clear()
        if state[0] == 1:
            if stateN == 0:
                self.axes.plot(data.axis_x, data.axis_y1, 'r', label = "A-x", alpha = 0.3)
                self.axes.set_xlabel("Muestras")
                self.axes.legend(loc = 'upper right')
            if stateN == 1:
                self.axes.scatter(data.axis_y1, data.axis_y1, color = 'r', label = u"Ángulo x")
                self.axes.set_xlabel(u"Ángulo x")
                self.axes.legend(loc = 'upper right')
            if stateN == 2:
                self.axes.scatter(data.axis_y2, data.axis_y1, color = 'r', label = u"Ángulo x")
                self.axes.set_xlabel(u"Ángulo y")
                self.axes.legend(loc = 'upper right')
            if stateN == 3:
                self.axes.scatter(data.axis_y3, data.axis_y1, color ='r', label = u"Ángulo x")
                self.axes.set_xlabel(u"Ángulo z")
                self.axes.legend(loc = 'upper right')
        if state[1] == 1:
            if stateN == 0:
                self.axes.plot(data.axis_x, data.axis_y2, 'b', label = "A-y")
                self.axes.set_xlabel("Muestras")
                self.axes.legend(loc = 'upper right')
            if stateN == 1:
                self.axes.scatter(data.axis_y1, data.axis_y2, color = 'b', label = u"Ángulo y")
                self.axes.set_xlabel(u"Ángulo x")
                self.axes.legend(loc = 'upper right')
            if stateN == 2:
                self.axes.scatter(data.axis_y2, data.axis_y2, color = 'b', label = u"Ángulo y")
                self.axes.set_xlabel(u"Ángulo y")
                self.axes.legend(loc = 'upper right')
            if stateN == 3:
                self.axes.scatter(data.axis_y3, data.axis_y2, color ='b', label = u"Ángulo y")
                self.axes.set_xlabel(u"Ángulo z")
                self.axes.legend(loc = 'upper right')
        if state[2] == 1:
            if stateN == 0:
                self.axes.plot(data.axis_x, data.axis_y3, 'g', label = "A-z")
                self.axes.set_xlabel("Muestras")
                self.axes.legend(loc = 'upper right')
            if stateN == 1:
                self.axes.scatter(data.axis_y1, data.axis_y3, color = 'g', label = u"Ángulo z")
                self.axes.set_xlabel(u"Ángulo x")
                self.axes.legend(loc = 'upper right')
            if stateN == 2:
                self.axes.scatter(data.axis_y2, data.axis_y3, color = 'g', label = u"Ángulo z")
                self.axes.set_xlabel(u"Ángulo y")
                self.axes.legend(loc = 'upper right')
            if stateN == 3:
                self.axes.scatter(data.axis_y3, data.axis_y3, color ='g', label = u"Ángulo z")
                self.axes.set_xlabel(u"Ángulo z")
                self.axes.legend(loc = 'upper right')
        if state[3] == 1:
            if stateN == 0:
                self.axes.plot(data.axis_x, data.axis_y4, 'c', label = "Ac-x")
                self.axes.set_xlabel("Muestras")
                self.axes.legend(loc = 'upper right')
            if stateN == 1:
                self.axes.scatter(data.axis_y4, data.axis_y4, color = 'c', label = u"Aceleración x")
                self.axes.set_xlabel(u"Aceleración x")
                self.axes.legend(loc = 'upper right')
            if stateN == 2:
                self.axes.scatter(data.axis_y5, data.axis_y4, color = 'b', label = u"Aceleración x")
                self.axes.set_xlabel(u"Aceleración y")
                self.axes.legend(loc = 'upper right')
            if stateN == 3:
                self.axes.scatter(data.axis_y6, data.axis_y4, color ='r', label = u"Aceleración x")
                self.axes.set_xlabel(u"Aceleración z")
                self.axes.legend(loc = 'upper right')
        if state[4] == 1:                            
            if stateN == 0:
                self.axes.plot(data.axis_x, data.axis_y5, 'm', label = "Ac-y")
                self.axes.set_xlabel("Muestras")
                self.axes.legend(loc = 'upper right')
            if stateN == 1:
                self.axes.scatter(data.axis_y4,data.axis_y5, color = 'k', label = u"Aceleración y")
                self.axes.set_xlabel(u"Aceleración x")
                self.axes.legend(loc = 'upper right')
            if stateN == 2:
                self.axes.scatter(data.axis_y5, data.axis_y5, color = 'g', label = u"Aceleración y")
                self.axes.set_xlabel(u"Aceleración y")
                self.axes.legend(loc = 'upper right')
            if stateN == 3:
                self.axes.scatter(data.axis_y6, data.axis_y5, color ='y', label = u"Aceleración y")
                self.axes.set_xlabel(u"Aceleración z")
                self.axes.legend(loc = 'upper right')
        if state[5] == 1:
            if stateN == 0:
                self.axes.plot(data.axis_x, data.axis_y6, 'y', label = "Ac-z")
                self.axes.set_xlabel("Muestras")
                self.axes.legend(loc = 'upper right')
            if stateN == 1:
                self.axes.scatter(data.axis_y4, data.axis_y6, color = 'm', label = u"Aceleración z")
                self.axes.set_xlabel(u"Aceleración x")
                self.axes.legend(loc = 'upper right')
            if stateN == 2:
                self.axes.scatter(data.axis_y5, data.axis_y6, color = 'g', label = u"Aceleración z")
                self.axes.set_xlabel(u"Aceleración y")
                self.axes.legend(loc = 'upper right')
            if stateN == 3:
                self.axes.scatter(data.axis_y6, data.axis_y6, color ='b', label = u"Aceleración z")
                self.axes.set_xlabel(u"Aceleración z")
                self.axes.legend(loc = 'upper right')
        if state[6] == 1:
            self.axes.plot(data.axis_x, data.axis_y7, 'k', label = "G-x")
            self.axes.legend(loc = 'upper right')
        if state[7] == 1:
            self.axes.plot(data.axis_x, data.axis_y8, 'b', label = "G-y")
            self.axes.legend(loc = 'upper right')
        if state[8] == 1:
            self.axes.plot(data.axis_x, data.axis_y9, 'c', label = "G-z")
            self.axes.legend(loc = 'upper right')
        if state[9] == 1:
            self.axes.plot(data.axis_x, data.axis_y10, 'g')
        if state[10] == 1:
            self.axes.plot(data.axis_x, data.axis_y11, 'r')
        if state[11] == 1:
            self.axes.plot(data.axis_x, data.axis_y12, 'm')

        if graph[0] == 0:
            c = 0.0
            cn = np.array(state).dot(np.array(data.Vmed))
            n = np.sum(state)
            if not(n==0):
                c = cn/n
            y_max = graph[2]+graph[1]
            y_min = graph[2]-graph[1]
            self.axes.set_ylim(y_min, y_max)

        if graph[0] == 1:
            self.axes.set_ylim(graph[2]-graph[1], graph[2]+graph[1])
            self.axes.set_xlim(graph[4]-graph[3], graph[4]+graph[3])

        self.draw()
