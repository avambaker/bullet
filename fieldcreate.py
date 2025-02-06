from PyQt5.QtWidgets import QLineEdit, QFormLayout, QVBoxLayout, QLabel, QAction, QDialog, QDialogButtonBox, QMessageBox, QComboBox, QTextEdit
from datetime import date
import pandas as pd
import json
from pathlib import Path


class FieldCreator(QDialog):
    def __init__(self, parent = None):
        """Create a form that creates or edits a row from user input"""
        super().__init__(parent)

        self.setWindowTitle("New Field")
        self.setGeometry(100, 100, 300, 400)

        self.layout = QFormLayout()
        self.layout.setSpacing(20)

        self.widget_dict = {
            'Header': QTextEdit(),
            'Paragraph': QTextEdit()
        }

        self.type_box = QComboBox()
        self.type_box.addItem("")
        for field in self.widget_dict.keys():
            self.type_box.addItem(field)
        self.type_box.currentTextChanged.connect(self.createInput)
        self.layout.addRow(QLabel("Field Type:"), self.type_box)
 
        # creating a dialog button for ok and cancel
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
 
        # connect to methods on button click
        self.buttonBox.accepted.connect(self.getInfo)
        self.buttonBox.rejected.connect(self.reject)
 
        # set a vertical layout with widgets and dialog buttons
        mainLayout = QVBoxLayout()
        mainLayout.addLayout(self.layout)
        mainLayout.addWidget(self.buttonBox)
        self.setLayout(mainLayout)

        self.last_field = self.type_box.currentText()

        self.show()

    def createInput(self):
        field_type = self.type_box.currentText()
        if field_type != self.last_field:
            if self.last_field in self.widget_dict:
                self.widget_dict[self.last_field].hide()
                self.layout.removeWidget(self.widget_dict[self.last_field])
                self.widget_dict[self.last_field].clear()
            if field_type in self.widget_dict:
                self.widget_dict[field_type].show()
                self.layout.addRow(self.widget_dict[field_type])
            self.last_field = field_type
        

    def getInfo(self):
        return