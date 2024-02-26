from PyQt5.QtWidgets import (QLineEdit)

class TextField:

        def __init__(self, initial_value=None, hint=None):
                self.text_field=QLineEdit()
                font = self.text_field.font()
                font.setPointSize(14)
                self.text_field.setFont(font)
                self.initial_value = initial_value
                self.hint = hint
                
                self.text = ''
                if not self.hint is None:
                        self.text_field.setPlaceholderText(self.hint) 
                if not self.initial_value is None:
                        self.text = initial_value
                        self.text_field.setText(self.initial_value)
                        
                self.text_field.textChanged.connect(self.text_changed)

        def set_text(self, text):
                self.text_field.setText(text)

        def get_text(self):
                return self.text

        def text_changed(self, text):
                self.text = text