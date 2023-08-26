# importing libraries
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

import networkx as nx

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

matplotlib.use('Qt5Agg')

class ModelSpecificationPlotterWindow(QDialog):
    def __init__(self, model_data, *args, **kwargs):
        super(ModelSpecificationPlotterWindow, self).__init__(*args, **kwargs)

        font = QFont()
        font.setPointSize(16)

        self.setGeometry(100, 100, 800, 600)
        self.center()
        self.setWindowTitle('S Plot')

        self.figure = plt.figure(figsize=(9, 9))
        self.canvas = FigureCanvas(self.figure)

        self.figure.clf()

        model = model_data
        G = nx.DiGraph()
        for state in model.keys():
            state = int(state)
            G.add_node(state, label=str(state))

        for state, transitions in model.items():
            for transition in transitions:
                # for transition in action.transitions:
                    state = int(state)
                    next_state = int(transition)
                    G.add_edge(state, next_state)


        nx.draw(G, with_labels = True, node_color ='green')
        self.canvas.draw_idle()

        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        # grid.addWidget(self.canvas, 0, 1, 9, 9) 
        self.setLayout(layout)

    def center(self):
        qr = self.frameGeometry()
        cp = QGuiApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())