from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5.QtWidgets import *

from PyQt5.QtCore import Qt

CANVAS_LAYOUT_RELATIVE_WIDTH = 100


class Canvas:
    """A canvas widget for displaying a matplotlib figure.

    - Attributes:
        - canvas (FigureCanvas): An instance of FigureCanvasQTAgg representing the canvas for displaying the figure.
        - vertical_layout (QVBoxLayout): A QVBoxLayout object for organizing the toolbar and canvas vertically.
        - toolbar (ToolBar): An instance of the ToolBar class representing the toolbar for the canvas.

    - Methods:
        - __init__(window): Initialize a Canvas object.

    """

    def __init__(self, config):
        self.canvas = FigureCanvas(Figure(figsize=(5, 3)))
        self.canvas.setFocusPolicy(Qt.StrongFocus)

        self.h_layout = QHBoxLayout()
        config.vertical_layout.addLayout(self.h_layout, CANVAS_LAYOUT_RELATIVE_WIDTH)

        self.h_layout.addWidget(self.canvas)

        