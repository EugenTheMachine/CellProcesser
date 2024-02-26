from PyQt5.QtWidgets import *

class CustomGraphicsScene(QGraphicsScene):
    def __init__(self):
        super().__init__()

class CustomGraphicsView(QGraphicsView):
    def __init__(self, scene):
        super().__init__(scene)
