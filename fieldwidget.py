from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout, QSizePolicy, QMenu, QAction
from PyQt5.QtCore import pyqtSignal, QSize
from PyQt5.QtGui import QIcon

class FieldWidget(QWidget):
    editClicked = pyqtSignal()  # Custom signal for edit action
    deleteClicked = pyqtSignal()  # Custom signal for edit action
    moveUp = pyqtSignal()
    moveDown = pyqtSignal()

    def __init__(self, field_id, field_type, content, parent=None):
        super().__init__(parent)

        self.id = field_id

        from JSONHandler import json_handler
        styles = {"Header": json_handler.get_css("Header"),
                  "Paragraph": json_handler.get_css("Paragraph")}

        # Create QLabel for header text
        self.label = QLabel(content)
        self.label.setStyleSheet(styles[field_type])
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.label.setWordWrap(True)

        # Create layout
        layout = QHBoxLayout()
        layout.addWidget(self.label, stretch=2)
        layout.addStretch()  # Push the button to the right
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

        # create context menu
        self.context_menu = QMenu(self)

        # Add actions
        self.edit_action = QAction("Edit Field", self)
        self.delete_action = QAction("Delete Field", self)
        self.move_up_action = QAction("Move Up", self)
        self.move_down_action = QAction("Move Down", self)

        self.edit_action.triggered.connect(self.editClicked.emit)
        self.delete_action.triggered.connect(self.deleteClicked.emit)
        self.move_up_action.triggered.connect(self.moveUp.emit)
        self.move_down_action.triggered.connect(self.moveDown.emit)

        self.context_menu.addAction(self.edit_action)
        self.context_menu.addAction(self.delete_action)
        self.context_menu.addAction(self.move_up_action)
        self.context_menu.addAction(self.move_down_action)
    
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
    
    def contextMenuEvent(self, event):
        self.context_menu.exec_(event.globalPos())
