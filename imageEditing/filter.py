import numpy as np

class Filter():
    def __init__(self, name: str, kernel: list, move: int, scale: float):
        self.kernel = kernel
        self.shape = int(np.sqrt(len(kernel)))
        if self.shape != np.sqrt(len(kernel)):
            raise SizeException()
        self.move = move
        self.scale = scale
        self.name = name

class SizeException(Exception):
    def __init__(self):
        super().__init__()
