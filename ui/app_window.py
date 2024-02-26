from matplotlib.figure import Figure
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np

from PyQt5.QtWidgets import (QVBoxLayout, QHBoxLayout, QMainWindow, QWidget, QMessageBox, QPushButton)

from ui.canvas.configurator import Configurator
from ui.canvas.imagespace import ImageSpace
from ui.settings import AXIS_MAX_SIZE, APP_WINDOW_MIN_WIDTH, APP_WINDOW_MIN_HEIGHT
from ui.menubar.menubar import *


class AppWindow(QMainWindow):

    def __init__(self, app):
        super().__init__()
        self.window_width, self.window_height = APP_WINDOW_MIN_WIDTH, APP_WINDOW_MIN_HEIGHT

        self.setMinimumSize(self.window_width, self.window_height)
        self.showMaximized()
        self.setStyleSheet('''
            QWidget {
                font-size: 32px;
            }
        ''')
        self.setWindowTitle('Cell detector')
        # self.figure = Figure(figsize=(20, 20))
        self.central_widget = QWidget()

        self.setCentralWidget(self.central_widget)
        self.horizontal_layout = QHBoxLayout(self.central_widget)

        self.all_primitives = []
        self.automata = None

        self.canvas_layout = ImageSpace(self)

        self.menubar = Menu_Bar(self)
        self.image_windows = []
        # self.lower()

        # self.ax = self.canvas_layout.canvas.figure.add_subplot()
        # Скрытие шкалы по оси X
        # self.ax.get_xaxis().set_visible(False)

        # Скрытие шкалы по оси Y
        # self.ax.get_yaxis().set_visible(False)
        # self.ax.axis('off')

        self.configurator_layout = Configurator(self)
        
    def closeEvent(self, event):
        for image_window in self.image_windows:
            image_window.close()

    # def automata_added(self, automata):
    #     self.automata = automata
    #     automata.plot(self.ax, self.canvas_layout.canvas)

    def show_error(self, title: str = "Error", text: str = "Unknown"):
        QMessageBox.critical(self, title, text)

    def show_info(self, title: str = "Error", text: str = "Unknown"):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setText(text)
        msgBox.setWindowTitle(title)
        msgBox.setStandardButtons(QMessageBox.Ok)
        
        # Execute the message box
        returnValue = msgBox.exec_()
        if returnValue == QMessageBox.Ok:
            print('OK clicked')

    def keyPressEvent(self, event):
        if event.modifiers() == Qt.ControlModifier:
            if event.key() == Qt.Key_A:
                if self.canvas_layout.view.hasFocus():
                    self.canvas_layout.view.scale(1.1, 1.1)
                elif self.canvas_layout.view2.hasFocus():
                    self.canvas_layout.view2.scale(1.1, 1.1)
                else:
                    pass
            elif event.key() == Qt.Key_S:
                if self.canvas_layout.view.hasFocus():
                    self.canvas_layout.view.scale(.9, .9)
                elif self.canvas_layout.view2.hasFocus():
                    self.canvas_layout.view2.scale(.9, .9)
                else:
                    pass
            elif event.key() == Qt.Key_Z:
                self.canvas_layout.setDisplayedImage2('CorrectedImage.bmp')
                self.configurator_layout.filterLabel.setText('-')
            elif event.key() == Qt.Key_Y:
                try:
                    self.canvas_layout.setDisplayedImage2('ResultImage.bmp')
                    text = self.configurator_layout.text
                    self.configurator_layout.filterLabel.setText(text)
                except Exception:
                    pass
        else:
            super().keyPressEvent(event)