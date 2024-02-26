from imageEditing.filter import *
from PyQt5.QtWidgets import *
from ui.text_field import *
from PyQt5.QtGui import *
import pickle
import os

class FilterCreator(QDialog):
    def __init__(self, win):
        super().__init__()
        self.setWindowTitle('Filter creator')
        layout = QVBoxLayout()
        self.nameTextField = TextField(hint='Enter filter name')
        self.kernelTextField = TextField(hint='Enter filter ker as "1 2 3..."')
        self.scaleTextField = TextField(hint='Enter filter ker scale factor')
        self.moveTextField = TextField(initial_value='0', hint='Enter filter move')
        self.createButton = QPushButton('Create')
        self.createButton.clicked.connect(self.createFilter)
        self.cancelButton = QPushButton('Cancel')
        self.cancelButton.clicked.connect(self.cancelCreation)
        layout.addWidget(self.nameTextField.text_field)
        layout.addWidget(self.kernelTextField.text_field)
        layout.addWidget(self.scaleTextField.text_field)
        layout.addWidget(self.moveTextField.text_field)
        self.buttonLayout = QHBoxLayout()
        layout.addLayout(self.buttonLayout)
        self.buttonLayout.addWidget(self.cancelButton)
        self.buttonLayout.addSpacing(10)
        self.buttonLayout.addWidget(self.createButton)
        self.setLayout(layout)
        self.setFixedSize(400,250)
        self.win = win

    def createFilter(self):
        name = self.nameTextField.get_text()
        if len(name) == 0:
            title = 'Empty name'
            text = 'Empty name. Please, enter the proper name.'
            self.win.show_error(title, text)
            return
        ker = self.kernelTextField.get_text().split()
        if len(ker) == 0:
            title = 'Empty kernel'
            text = 'The kernel is empty. Please, correct it'
            self.win.show_error(title, text)
            return
        for i in range(len(ker)):
            try:
                ker[i] = int(ker[i])
            except Exception:
                self.win.show_error('title', 'text .......')
                return
        if np.sqrt(len(ker)) != int(np.sqrt(len(ker))):
            title = 'Invalid kernel'
            text = 'The kernel has invalid size. Please, correct it'
            self.win.show_error(title, text)
            return
        try:
            move = int(self.moveTextField.get_text())
        except Exception:
            title = 'Invalid move value'
            text = 'The move has invalid value. Please, correct it'
            self.win.show_error(title, text)
            return
        if len(self.moveTextField.get_text()) == 0:
            title = 'Empty move'
            text = 'The move has empty value. Please, correct it'
            self.win.show_error(title, text)
            return
        
        try:
            scale = float(self.scaleTextField.get_text())
        except Exception:
            title = 'Invalid scale value'
            text = 'The scale has invalid value. Please, correct it'
            self.win.show_error(title, text)
            return
        if len(self.scaleTextField.get_text()) == 0:
            title = 'Empty scale'
            text = 'The scale has empty value. Please, correct it'
            self.win.show_error(title, text)
            return
        new_filter = Filter(name, ker, move, scale)
        self.serialize(new_filter)

    def serialize(self, filter: Filter):
        path = os.path.join('filters', '{}.pkl'.format(filter.name))
        with open(path, 'wb') as file:
            pickle.dump(filter, file)
        self.close()

    def cancelCreation(self):
        self.close()

class FilterDeleter(QDialog):
    def __init__(self, win):
        super().__init__()
        layout = QVBoxLayout()
        self.setWindowTitle('Filter deleter')
        self.nameTextField = TextField(hint='Enter filter name')
        self.deleteButton = QPushButton('Delete')
        self.deleteButton.clicked.connect(self.deleteFilter)
        self.cancelButton = QPushButton('Cancel')
        self.cancelButton.clicked.connect(self.cancelCreation)
        layout.addWidget(self.nameTextField.text_field)
        self.buttonLayout = QHBoxLayout()
        layout.addLayout(self.buttonLayout)
        self.buttonLayout.addWidget(self.cancelButton)
        self.buttonLayout.addSpacing(10)
        self.buttonLayout.addWidget(self.deleteButton)
        self.setLayout(layout)
        self.setFixedSize(400,150)
        self.win = win

    def deleteFilter(self):
        name = self.nameTextField.get_text()
        if os.path.exists(os.path.join('filters', f'{name}.pkl')):
            os.remove(os.path.join('filters', f'{name}.pkl'))
            self.close()
        else:
            title = 'Invalid filter name'
            text = 'The filter name is invalid. PLease, try again.'
            self.win.show_error(title=title, text=text)

    def cancelCreation(self):
        self.close()