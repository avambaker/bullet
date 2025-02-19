from PyQt5.QtWidgets import (QVBoxLayout, QLabel, QDialog,
                             QDialogButtonBox, QTextEdit)


class FieldEditor(QDialog):
    def __init__(self, field_type, field_content, parent = None):
        """Create a form that creates or edits a row from user input"""
        super().__init__(parent)

        # set up variables
        self.field_type = field_type
        self.field_content = field_content

        self.widget_dict = {
            'Header': QTextEdit(),
            'Paragraph': QTextEdit()
        }

        self.method_dict = {
            'Header': self.getHeaderText,
            'Paragraph': self.getParagraphText
        }

        # configure window details
        self.setWindowTitle(field_type)
        self.setGeometry(100, 100, 300, 400)

        self.editor = self.widget_dict.get(self.field_type)
        self.editor.setText(self.field_content)
 
        # creating a dialog button for ok and cancel
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
 
        # connect to methods on button click
        self.buttonBox.accepted.connect(self.getInfo)
        self.buttonBox.rejected.connect(self.reject)

        # set a vertical layout with widgets and dialog buttons
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.addWidget(QLabel(f"Edit {field_type}:"))
        layout.addWidget(self.editor)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)

        self.show()

    def getInfo(self):
        self.new_val = self.method_dict[self.field_type]()
        super().accept()
    
    def getHeaderText(self):
        return self.editor.toPlainText()

    def getParagraphText(self):
        return self.editor.toPlainText()