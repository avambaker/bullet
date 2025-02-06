from PyQt5.QtWidgets import QLineEdit, QFormLayout, QVBoxLayout, QLabel, QAction, QDialog, QDialogButtonBox, QMessageBox, QComboBox, QTextEdit
from datetime import date
import pandas as pd
import json
from pathlib import Path


class FieldEditor(QDialog):
    def __init__(self, field_type = "", field_content = "", parent = None):
        """Create a form that creates a new row from user input"""
        super().__init__(parent)

        # set up variables
        self.field_type = field_type
        self.field_content = field_content

        self.widget_dict = {
            'Header': QLineEdit(),
            'Paragraph': QTextEdit()
        }

        # configure window details
        if field_type != "":
            self.setWindowTitle(field_type)
        else:
            self.setWindowTitle("New Field")
        self.setGeometry(100, 100, 300, 400)

        layout = QFormLayout()
        layout.setSpacing(20)

        if field_type != '':
            editor = self.widget_dict.get(self.field_type)
            editor.setText(self.field_content)
            layout.addRow(QLabel(f"Edit {field_type}:"), editor)

        if field_type == '':
            type_box = QComboBox()
            type_box.addItem("")
            type_box.addItem("Header")
            type_box.addItem("Paragraph")
            layout.addRow(QLabel("Field Type:"), type_box)
 
        # creating a dialog button for ok and cancel
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
 
        # connect to methods on button click
        self.buttonBox.accepted.connect(self.getInfo)
        self.buttonBox.rejected.connect(self.reject)
 
        # set a vertical layout with widgets and dialog buttons
        mainLayout = QVBoxLayout()
        mainLayout.addLayout(layout)
        mainLayout.addWidget(self.buttonBox)
        self.setLayout(mainLayout)

        self.show()

    def getInfo(self):
        return