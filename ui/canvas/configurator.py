from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('Qt5Agg')
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from ui.text_field import *
from ui.separator.separator import *
from ui.canvas.canvas import *
# from ui.menubar.menubar import *
# from ui.fileDialog.fileDialog import *
from ui.slider.slider import *
from imageEditing.imageEditing import *

CONFIGURATOR_LAYOUT_RELATIVE_WIDTH = 25

class Configurator(QWidget):

    def init_UI(self, window):
        # self.canvas = FigureCanvas(Figure(figsize=(5, 3)))
        self.win = window

        self.vertical_layout = QVBoxLayout()
        window.horizontal_layout.addLayout(self.vertical_layout, CONFIGURATOR_LAYOUT_RELATIVE_WIDTH)

        self.vertical_layout.addSpacing(100)
        self.titleLabel = QLabel("Alive cells (%):")
        self.titleLabel.setAlignment(Qt.AlignCenter)
        self.vertical_layout.addWidget(self.titleLabel)
        self.vertical_layout.addSpacing(75)

        self.text = '15.3'
        self.filterLabel = QLabel(self.text)
        self.filterLabel.setAlignment(Qt.AlignCenter)
        self.vertical_layout.addWidget(self.filterLabel)

        self.vertical_layout.addSpacing(75)

        self.percButton = QPushButton('Calculate %')
        self.vertical_layout.addWidget(self.percButton)
        # self.percButton.setAlignment(Qt.AlignCenter)
        self.vertical_layout.addSpacing(40)

        self.vertical_layout.addSpacing(800)


        # self.valueLabel = QLabel('Scale by factor: 2.0')
        # self.vertical_layout.addWidget(self.valueLabel)

        # self.scaling_slider = Slider(self.win)
        # self.scaling_slider.slider.valueChanged.connect(self.scalingValueChanged)
        # self.vertical_layout.addWidget(self.scaling_slider.slider)
        
        # self.vertical_layout.addWidget(Separator())

        # # canvas part
        # self.figure = Figure(figsize=(20, 20))
        # self.central_widget = QWidget()
        # self.canvas_layout = Canvas(self)
        # # self.plots = []
        # self.ax = self.canvas_layout.canvas.figure.add_subplot()
        # self.ax.set_xticks([])
        # self.ax.set_yticks([])
        # self.ax.set_title('Bezier curve')
        # self.mouseFlag = 0  # whether mouse left button is pressed
        # self.activePoint = None
        # self.setDefaultCanvas()

        
        #--------------------------------------------------------------------------------#

    def setDefaultCanvas(self):
        self.A_x, self.A_y = .25, .25
        self.B_x, self.B_y = .75, .75
        length = 100
        t = np.linspace(0, 1, length).T
        A = np.array([[-1, 3, -3, 1],
                      [3, -6, 3, 0],
                      [-3, 3, 0, 0], 
                      [1, 0, 0, 0]])
        kx = A @ np.array([0, self.A_x, self.B_x, 1])
        kx = np.tile(kx, (length, 1))
        ky = A @ np.array([0, self.A_y, self.B_y, 1])
        ky = np.tile(ky, (length, 1))
        ts = np.stack((t**3, t**2, t, t**0), axis=1)
        # print(ts.shape)
        self.bezier_xs = np.sum(ts * kx, axis=1)
        self.bezier_ys = np.sum(ts * ky, axis=1)
        self.curve = self.ax.plot(self.bezier_xs, self.bezier_ys)
        self.A = self.ax.scatter(self.A_x, self.A_y, color='b', picker=True)
        self.B = self.ax.scatter(self.B_x, self.B_y, color='b', picker=True)
        # self.ax.legend()
        self.canvas_layout.canvas.draw()
        self.canvas_layout.canvas.mpl_connect('motion_notify_event', self.on_move)
        self.canvas_layout.canvas.mpl_connect('button_press_event', self.on_press)
        self.canvas_layout.canvas.mpl_connect('button_release_event', self.on_release)
        self.canvas_layout.canvas.mpl_connect('key_press_event', self.on_click)
        self.ax.set_xlim(0, 1)
        self.ax.set_ylim(0, 1)

    def setBezierCurve(self):
        self.ax.clear()
        self.A = self.ax.scatter(self.A_x, self.A_y, color='b', picker=True)
        self.B = self.ax.scatter(self.B_x, self.B_y, color='b', picker=True)
        length = 100
        t = np.linspace(0, 1, length).T
        A = np.array([[-1, 3, -3, 1],
                      [3, -6, 3, 0],
                      [-3, 3, 0, 0], 
                      [1, 0, 0, 0]])
        kx = A @ np.array([0, self.A_x, self.B_x, 1])
        kx = np.tile(kx, (length, 1))
        ky = A @ np.array([0, self.A_y, self.B_y, 1])
        ky = np.tile(ky, (length, 1))
        ts = np.stack((t**3, t**2, t, t**0), axis=1)
        # print(ts.shape)
        self.bezier_xs = np.sum(ts * kx, axis=1)
        self.bezier_ys = np.sum(ts * ky, axis=1)
        self.curve = self.ax.plot(self.bezier_xs, self.bezier_ys)
        # self.curve.set_xdata(self.bezier_xs)
        # self.curve.set_ydata(self.bezier_ys)
        self.canvas_layout.canvas.draw()
        return [self.bezier_xs, self.bezier_ys]

    def on_click(self, event):
        if event.key == 'a':
            self.activePoint = self.A
        elif event.key == 'b':
            self.activePoint = self.B

    def on_move(self, event):        
        if event.inaxes is not None and self.mouseFlag and self.activePoint is not None:
            if self.activePoint == self.A:
                self.A_x, self.A_y = event.xdata, event.ydata
                self.A.set_offsets([(self.A_x, self.A_y)])
                self.A.figure.canvas.draw()
                bxs, bys = self.setBezierCurve()
                coefficients = np.polyfit(bxs, bys, 10)
                p = np.poly1d(coefficients)
                new_img = gammaCorrect(self.win.canvas_layout.image_data, p)
                self.win.canvas_layout.setCorrectedImage(im.fromarray(new_img.astype('uint8')))
                self.win.canvas_layout.setDisplayedImage2('CorrectedImage.bmp')
            elif self.activePoint == self.B:
                self.B_x, self.B_y = event.xdata, event.ydata
                self.B.set_offsets([(self.B_x, self.B_y)])
                self.B.figure.canvas.draw()
                bxs, bys = self.setBezierCurve()
                coefficients = np.polyfit(bxs, bys, 10)
                p = np.poly1d(coefficients)
                new_img = gammaCorrect(self.win.canvas_layout.image_data, p)
                self.win.canvas_layout.setCorrectedImage(im.fromarray(new_img.astype('uint8')))
                self.win.canvas_layout.setDisplayedImage2('CorrectedImage.bmp')
            else:
                pass

    def on_press(self, event):
        if event.button == 1:
            self.mouseFlag = 1

    def on_release(self, event):
        if event.button == 1:
            self.mouseFlag = 0

    


    def scalingValueChanged(self):
        self.valueLabel.setText('Scale by factor: {}'.format(self.scaling_slider.value))
        if self.win.menubar.filter is not None:
            self.win.menubar.applyFilter()

    def __init__(self, window):
        super().__init__()
        self.init_UI(window)



    