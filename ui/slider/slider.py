from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from ui.fileDialog.fileDialog import *
from ui.graphicscene.graphicscene import *
from imageEditing.imageEditing import *

class Slider():
    def __init__(self, win):
        super().__init__()
        self.initUI(win)

    def initUI(self, win):
        self.win = win
        self.slider = QSlider()
        self.slider.setOrientation(Qt.Horizontal)
        self.slider.setMinimum(1)
        self.slider.setMaximum(64)
        self.slider.setSingleStep(1)
        self.slider.setValue(32)
        self.value = 1
        self.scaleFactor = .25
        self.slider.valueChanged.connect(self.onSliderChange)

    def onSliderChange(self, value):
        self.value = value * self.scaleFactor
        self.win.menubar.filter.scale = self.value
        result = applyFilter(self.win.canvas_layout.image, self.win.menubar.filter)        
        self.win.canvas_layout.setResultImage(result)
        self.win.canvas_layout.setDisplayedImage('ResultImage.bmp')

