from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout, QSizePolicy
from PyQt5.QtCore import pyqtSignal, QSize
from PyQt5.QtGui import QIcon

class FieldWidget(QWidget):
    editClicked = pyqtSignal()  # Custom signal for edit action
    deleteClicked = pyqtSignal()  # Custom signal for edit action

    def __init__(self, field_type, content, parent=None):
        super().__init__(parent)

        from JSONHandler import json_handler
        styles = {"Header": json_handler.get_css("Header"),
                  "Paragraph": json_handler.get_css("Paragraph")}

        # Create QLabel for header text
        self.label = QLabel(content)
        self.label.setStyleSheet(styles[field_type])
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.label.setWordWrap(True)
        
        # Create QPushButtons for editing and delete
        self.edit_button = self.create_button("icons/pencil.png")
        self.delete_button = self.create_button("icons/delete.png")
        
        # Connect the buttons' clicked signal
        self.edit_button.clicked.connect(self.editClicked.emit)
        self.delete_button.clicked.connect(self.deleteClicked.emit)

        # Create layout
        layout = QHBoxLayout()
        layout.addWidget(self.label, stretch=2)
        layout.addStretch()  # Push the button to the right
        layout.addWidget(self.edit_button)
        layout.addWidget(self.delete_button)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
    
    def create_button(self, icon_path):
        button = QPushButton()
        button.setIcon(QIcon(icon_path))  # Set your icon path
        button.setFixedSize(QSize(30, 30))
        button.setIconSize(QSize(10, 10))
        button.setFlat(True)  # Make button background invisible
        return button

    def setText(self, text):
        """Update the label text."""
        self.label.setText(text)
