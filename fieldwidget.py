from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout, QSizePolicy
from PyQt5.QtCore import pyqtSignal, QSize
from PyQt5.QtGui import QIcon

class FieldWidget(QWidget):
    editClicked = pyqtSignal()  # Custom signal for edit action

    def __init__(self, field_type, content, parent=None):
        super().__init__(parent)

        from JSONHandler import json_handler
        styles = {"Header": json_handler.get_css("Header"),
                  "Paragraph": json_handler.get_css("Paragraph")}

        # Create QLabel for header text
        self.label = QLabel(content)
        self.label.setStyleSheet(styles[field_type])
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        print(styles[field_type])
        self.label.setWordWrap(True)
        
        # Create QPushButton for edit icon
        self.edit_button = QPushButton()
        self.edit_button.setIcon(QIcon("pencil_icon.png"))  # Set your icon path
        self.edit_button.setMinimumSize(QSize(10, 10))
        self.edit_button.setIconSize(QSize(10, 10))
        self.edit_button.setFlat(True)  # Make button background invisible
        self.edit_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.edit_button.setFlat(True)
        
        # Connect the button's clicked signal
        self.edit_button.clicked.connect(self.editClicked.emit)

        # Create layout
        layout = QHBoxLayout()
        layout.addWidget(self.label)
        layout.addStretch()  # Push the button to the right
        layout.addWidget(self.edit_button)
        layout.setContentsMargins(0, 0, 0, 0)
        # Set stretch factors
        layout.setStretch(0, 1)  # Stretch label
        layout.setStretch(1, 0)  # No stretch for button
        self.setLayout(layout)

    def setText(self, text):
        """Update the label text."""
        self.label.setText(text)
