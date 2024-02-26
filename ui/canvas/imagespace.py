import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap, QPainter, QColor
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from ui.graphicscene.graphicscene import *
from PIL import Image as im
import numpy as np

CANVAS_LAYOUT_RELATIVE_WIDTH = 75


class ImageSpace:
    def __init__(self, window):
        self.vertical_layout = QHBoxLayout()
        window.horizontal_layout.addLayout(self.vertical_layout, CANVAS_LAYOUT_RELATIVE_WIDTH)
        self.view = CustomGraphicsView(window)
        self.scene = CustomGraphicsScene()
        self.view.setScene(self.scene)
        self.vertical_layout.addWidget(self.view)

        # the second view below, temporary commented

        # self.view2 = CustomGraphicsView(window)
        # self.scene2 = CustomGraphicsScene()
        # self.view2.setScene(self.scene2)
        # self.vertical_layout.addWidget(self.view2)

        self.image = None
        self.image_data = None
        self.result_image = None
        self.result_image_data = None
        self.displayed_image = None
        self.displayed_image_data = None
        self.corrected_image = None
        self.corrected_image_data = None

    def setDisplayedImage(self, path):
        self.displayed_image = im.open(path)
        self.displayed_image_data = np.array(self.displayed_image).astype('float32')
        pixmap = QPixmap(path)
        item = QGraphicsPixmapItem(pixmap)
        self.scene.clear()
        self.view.setSceneRect(0, 0, pixmap.width(), pixmap.height())
        self.scene.addItem(item)

    def setDisplayedImage2(self, path):
        self.displayed_image = im.open(path)
        self.displayed_image_data = np.array(self.displayed_image).astype('float32')
        pixmap = QPixmap(path)
        item = QGraphicsPixmapItem(pixmap)
        self.scene2.clear()
        self.view2.setSceneRect(0, 0, pixmap.width(), pixmap.height())
        self.scene2.addItem(item)

    def setImage(self, image):
        self.image = image
        image.save('Image.bmp')
        self.image_data = np.array(self.image).astype('float32')

    def setResultImage(self, image):
        self.result_image = image
        image.save('ResultImage.bmp')
        self.result_image_data = np.array(self.result_image).astype('float32')

    def setCorrectedImage(self, image):
        self.corrected_image = image
        image.save('CorrectedImage.bmp')
        self.corrected_image_data = np.array(self.corrected_image).astype('float32')
