from PyQt5.QtWidgets import QWidget, QFormLayout, QVBoxLayout, QLabel, QStackedWidget, QDialog, QDialogButtonBox, QMessageBox, QComboBox, QTextEdit
from datetime import date
import pandas as pd
import json
from pathlib import Path


class WidgetCreator(QDialog):
    def __init__(self, parent = None):
        """Create a form that creates or edits a row from user input"""
        super().__init__(parent)

        self.setWindowTitle("New Field")
        self.setGeometry(100, 100, 300, 400)

        self.widget_dict = {
            '': QWidget(),
            'Header': QTextEdit(),
            'Paragraph': QTextEdit(),
            'Task': QTextEdit()
        }

        self.type_box = QComboBox()
        for field in self.widget_dict.keys():
            self.type_box.addItem(field)
        self.type_box.currentTextChanged.connect(self.createInput)
        self.type_box.setCurrentIndex(0)

        form_layout = QFormLayout()
        form_layout.setSpacing(20)
        form_layout.addRow(QLabel("Field Type:"), self.type_box)

        self.stacked_widget = QStackedWidget()
        # add all the input widgets
        for key in self.widget_dict.keys():
            self.stacked_widget.addWidget(self.widget_dict[key])
        self.stacked_widget.setCurrentWidget(self.widget_dict[""])
 
        # creating a dialog button for ok and cancel
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
 
        # connect to methods on button click
        self.buttonBox.accepted.connect(self.getInfo)
        self.buttonBox.rejected.connect(self.reject)
 
        # set a vertical layout with widgets and dialog buttons
        main_layout = QVBoxLayout()
        main_layout.addLayout(form_layout)
        main_layout.addWidget(self.stacked_widget)
        main_layout.addWidget(self.buttonBox)
        self.setLayout(main_layout)

        self.last_field = ""

        self.show()

    def createInput(self):
        """Show/hide widgets based on the selected field type"""
        self.type_box.blockSignals(True)  # Prevent unintended signals
        field_type = self.type_box.currentText()
        #print(f"[DEBUG] User selected: {field_type}")

        if field_type in self.widget_dict:
            self.stacked_widget.setCurrentWidget(self.widget_dict[field_type])

        self.last_field = field_type
        self.type_box.blockSignals(False)  # Re-enable signals

        """field_type = self.type_box.currentText()

        if field_type != self.last_field:
            if self.last_field != "":
                self.widget_dict[self.last_field].clear()
            self.stacked_widget.setCurrentWidget(self.widget_dict[field_type])
            self.last_field = field_type"""
    
    def getTextEditText(self):
        return self.stacked_widget.currentWidget().toPlainText()

    def getInfo(self):
        #print(f"Before setting: self.w_type = {self.type_box.currentText()}")
        self.w_type = self.type_box.currentText()
        #print(f"After setting: self.w_type = {self.w_type}")
        method_dict = {
            'Header': self.getTextEditText,
            'Paragraph': self.getTextEditText,
            'Task': self.getTextEditText,
            '': lambda: ''
        }
        self.w_type = self.type_box.currentText()
        self.w_content = method_dict[self.w_type]()
        super().accept()