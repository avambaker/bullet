from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QPushButton, QLabel, QLineEdit, QDateTimeEdit
from PyQt5.QtCore import QDateTime

class EditDialog(QDialog):
    def __init__(self, title, attribute, content, parent=None):
        super().__init__(parent)

        self.attribute = attribute
        self.setWindowTitle(f"Change {attribute} of: {title}")
        self.setMinimumSize(300, 200)  # Set the minimum size

        self.widget_dict = {
            'Title': QLineEdit(),
            'Description': QTextEdit(),
            'Deadline': QDateTimeEdit()
        }

        self.fetch_dict = {
            'Title': self.getLineEditText,
            'Description': self.getTextEditText,
            'Deadline': self.getDate
        }

        self.set_dict = {
            'Title': self.setLineEdit,
            'Description': self.setTextEdit,
            'Deadline': self.setDate
        }

        # Create a QTextEdit widget
        self.data_input = self.widget_dict[attribute]
        self.set_dict[attribute](content)
        
        # Create OK and Cancel buttons
        self.ok_button = QPushButton("OK")
        self.cancel_button = QPushButton("Cancel")

        # Layout to arrange the widgets
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Edit:"))
        layout.addWidget(self.data_input)
        layout.addWidget(self.ok_button)
        layout.addWidget(self.cancel_button)
        self.setLayout(layout)

        # Connect buttons to actions
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

    def get_text(self):
        return self.fetch_dict[self.attribute]()
    
    def getLineEditText(self):
        return self.data_input.text()
    
    def getDate(self):
        new_date = self.data_input.dateTime()
        return new_date.toString("ddd MM/dd/yyyy h:mm AP")

    def getTextEditText(self):
        return self.data_input.toPlainText()
    
    def setLineEdit(self, content):
        self.data_input.setText(content)
    
    def setTextEdit(self, content):
        self.data_input.setPlainText(content)
    
    def setDate(self, content):
        qdatetime = QDateTime.fromString(content, "ddd MM/dd/yyyy h:mm AP")
        if qdatetime.isValid():
            self.data_input.setDateTime(qdatetime)

