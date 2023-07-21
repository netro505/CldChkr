from components.scroll_label import ScrollLabel

import numpy as np
from utils.stormpy_util import StormpyUtil

import os

import json
import ast

# importing libraries
from PyQt6.QtWidgets import *
from PyQt6 import QtCore, QtGui
from PyQt6.QtGui import *
from PyQt6.QtCore import *
import pyqtgraph as pg
import random

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

import igraph as ig
import matplotlib.pyplot as plt
import matplotlib

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import networkx as nx

class VerifyWindow(QDialog):
    def __init__(self, model_data, *args, **kwargs):
        super(VerifyWindow, self).__init__(*args, **kwargs)

        font = QFont()
        font.setPointSize(16)

        self.setGeometry(100, 100, 800, 600)
        self.center()
        self.setWindowTitle('S Plot')

        # grid = QGridLayout()

        self.figure = plt.figure(figsize=(9, 9))
        self.canvas = FigureCanvas(self.figure)

        self.figure.clf()
        # B = nx.Graph()
        # B.add_nodes_from([1, 2, 3, 4], bipartite=0)
        # B.add_nodes_from(['a', 'b', 'c', 'd', 'e'], bipartite=1)
        # B.add_edges_from([(1, 'a'), (2, 'c'), (3, 'd'), (3, 'e'), (4, 'e'), (4, 'd')])

        # X = set(n for n, d in B.nodes(data=True) if d['bipartite'] == 0)
        # Y = set(B) - X

        # X = sorted(X, reverse=True)
        # Y = sorted(Y, reverse=True)

        # pos = dict()
        # pos.update( (n, (1, i)) for i, n in enumerate(X) ) # put nodes from X at x=1
        # pos.update( (n, (2, i)) for i, n in enumerate(Y) ) # put nodes from Y at x=2
        # model = model_data
        # G = nx.DiGraph()
        # for state in model.keys():
        #     state = int(state)
        #     G.add_node(state, label=str(state))

        # for state, transitions in model.items():
        #     for transition in transitions:
        #         # for transition in action.transitions:
        #             state = int(state)
        #             next_state = int(transition)
        #             G.add_edge(state, next_state)


        # nx.draw(G, with_labels = True, node_color ='green')

        ax1 = self.figure.add_subplot(211)
        x1 = list(range(0,model_data[-1],10))
        y1 = [i**0.5 for i in x1]

        # ax1.axvline(x=28, color="r")
        # ax1.axvline(x=42, color="r")
        
        ax1.set_xticks(x1)
        ax1.set_xlabel('States')
        ax1.set_ylabel('Expected steps')
        # ax1.set_title("Music Shuffle")
        
        ax1.plot(range(1, model_data[-1]), model_data[1:], linewidth=2)
        # ax1.vlines(10, 0, 'r')

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