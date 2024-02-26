from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from ui.fileDialog.fileDialog import *
from PIL import Image as im
from imageEditing.filtercreator import *
from imageEditing.imageEditing import *
from ui.canvas.imagespace import *

class Menu_Bar(QWidget):
    def __init__(self, window):
        super().__init__()
        self.init_ui(window)

    def init_ui(self, window):
        self.win = window
        self.filter = None

        self.openAction = QAction('Open', self)
        self.openAction.triggered.connect(self.openImage)

        self.saveAction = QAction('Save as', self)
        self.saveAction.triggered.connect(self.saveImageAs)

        self.applyFilterAction = QAction('Apply filter', self)
        self.applyFilterSubmenu = QMenu('Apply filter', self)
        self.filters = []
        actions = os.listdir('filters')
        for action in actions:
            filter = QAction(action.split('.')[0], self)
            filter.triggered.connect(lambda checked, file=action.split('.')[0]: self.applyFilter(file))
            self.filters.append(filter)
        for i in range(len(self.filters)):
            self.applyFilterSubmenu.addAction(self.filters[i])
        self.applyFilterAction.setMenu(self.applyFilterSubmenu)
        
        self.addFilterAction = QAction('Add filter', self)
        self.addFilterAction.triggered.connect(self.addFilter)

        self.deleteFilterAction = QAction('Delete filter', self)
        self.deleteFilterAction.triggered.connect(self.deleteFilter)

        self.infoAction = QAction('Info', self)
        self.infoAction.triggered.connect(self.info_on_clicked)


        self.menubar = self.win.menuBar()
        self.fileMenu = self.menubar.addMenu('File')
        self.fileMenu.addAction(self.openAction)
        self.fileMenu.addAction(self.saveAction)

        self.fileMenu = self.menubar.addMenu('Settings')

        # self.filterMenu = self.menubar.addMenu('Filters')
        # self.filterMenu.addAction(self.applyFilterAction)
        # self.filterMenu.addAction(self.addFilterAction)
        # self.filterMenu.addAction(self.deleteFilterAction)

        self.infoMenu = self.menubar.addMenu('Info')
        self.infoMenu.addAction(self.infoAction)


    def openImage(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_dialog = fileDialog(self.win)
        file_path, _ = file_dialog.getOpenFileName(self, "Open image", "", "Images (*.png *.jpg *.bmp);;All Files (*)", options=options)
        if file_path:
            self.win.canvas_layout.setCorrectedImage(im.open(file_path))
            self.win.canvas_layout.setDisplayedImage('CorrectedImage.bmp')
            self.win.canvas_layout.setImage(im.open('CorrectedImage.bmp'))
        if os.path.exists('ResultImage.bmp'):
            os.remove('ResultImage.bmp')

    def saveImageAs(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить изображение", "", "Images (*.png *.jpg *.bmp);;Все файлы (*)", options=options)

        if file_path:
            try:
                img_array = self.win.canvas_layout.result_image_data.astype('uint8')
                img = im.fromarray(img_array)
                img.save(file_path)
            except Exception:
                # print('here')
                try:
                    img_array = self.win.canvas_layout.image_data.astype('uint8')
                    img = im.fromarray(img_array)
                    img.save(file_path)
                except Exception:
                    print('here')

    def applyFilter(self, text=None):
        if text is not None:
            with open(os.path.join('filters', '{}.pkl'.format(text)), 'rb') as file:
                filter = pickle.load(file)
            self.filter = filter
        
        result = applyFilter(self.win.canvas_layout.corrected_image, self.filter)
        
        self.win.canvas_layout.setResultImage(result)
        self.win.canvas_layout.setDisplayedImage2('ResultImage.bmp')
        self.win.configurator_layout.text = text
        self.win.configurator_layout.filterLabel.setText(text)

    def addFilter(self):
        filter_creator = FilterCreator(self.win)
        filter_creator.exec_()
        self.applyFilterSubmenu.clear()
        self.filters = []
        actions = os.listdir('filters')
        for action in actions:
            filter = QAction(action.split('.')[0], self)
            filter.triggered.connect(lambda checked, file=action.split('.')[0]: self.applyFilter(file))
            self.filters.append(filter)    
        for i in range(len(self.filters)):
            self.applyFilterSubmenu.addAction(self.filters[i])

    def deleteFilter(self):
        try:
            filter_deleter = FilterDeleter(self.win)
            filter_deleter.exec_()
        except Exception:
            title = 'Invalid filter name'
            text = 'The filter name is invalid. PLease, try again.'
            self.win.show_error(title=title, text=text)


    def info_on_clicked(self):
        text = '''This application enables users to change image color map by using another 'source' image as the starting point.
        To start working, just open the source and the target images using the corresponding buttons in the upper 'File' menu option.
        As a result, you will have source, target and result images opened in separated scalable sub-windows; you are free to move them wherever you need to.
        Please, use Ctrl+A and Ctrl+S key combinations to scale the chosen image (zoom in and zoom out correspondingly).'''
        self.win.show_info('Info', text)
