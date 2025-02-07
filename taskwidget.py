from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QCheckBox, QPushButton, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

class TaskWidget(QWidget):
    def __init__(self, databasecontroller, title, parent=None):
        super().__init__(parent)

        self.db_controller = databasecontroller
        

        from JSONHandler import json_handler
        self.styles = {"Task Header": json_handler.get_css("Task Header"),
                  "Task Content": json_handler.get_css("Task Content"),
                  "Task Widget": json_handler.get_css("Task Widget")}

        # Main Layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # Row Layout (Checkbox + Title)
        self.row_widget = QWidget()
        self.row_layout = QHBoxLayout(self.row_widget)
        self.row_layout.setContentsMargins(5, 5, 5, 5)
        
        self.checkbox = QCheckBox()
        self.title_label = QLabel(title) # change this later
        self.title_label.setStyleSheet(self.styles['Task Header'])
        
        self.row_layout.addWidget(self.checkbox)
        self.row_layout.addWidget(self.title_label)
        self.row_layout.setSpacing(15)
        self.row_layout.addStretch()

        # Expand/Collapse Button
        self.toggle_button = QPushButton("▼")
        self.toggle_button.setFlat(True)  # Make button background invisible
        self.toggle_button.clicked.connect(self.toggle_description)
        self.row_layout.addWidget(self.toggle_button)

        self.main_layout.addWidget(self.row_widget)

        # Click anywhere on the row to expand/collapse
        self.row_widget.mousePressEvent = self.toggle_on_click

        # **Spacer to Align with Title**
        self.spacer_width = self.checkbox.sizeHint().width() + 10  # Get the checkbox's width

        # set up fields
        self.field_container = QWidget()
        self.field_container.setStyleSheet(self.styles["Task Widget"])
        self.field_container.setVisible(False)
        self.main_layout.addWidget(self.field_container)

        # create layout
        self.field_layout = QVBoxLayout()
        self.field_container.setLayout(self.field_layout)


        self.setStyleSheet(self.styles["Task Widget"])
        self.add_field(title) # change this later

    def toggle_description(self):
        """Toggles the visibility of the description."""
        self.field_container.setVisible(self.field_container.isHidden())
        self.toggle_button.setText("▲" if not self.field_container.isHidden() else "▼")

    def toggle_on_click(self, event):
        self.toggle_button.toggle()
        self.toggle_description()
    
    def add_field(self, content):
        description_layout = QHBoxLayout()
        description_layout.setContentsMargins(0, 0, 0, 0)

        spacer_widget = QWidget()
        spacer_widget.setFixedWidth(self.spacer_width)  # Match title width

        description_label = QLabel(content)
        description_label.setWordWrap(True)
        description_label.setStyleSheet(self.styles['Task Content'])

        description_layout.addWidget(spacer_widget)  # Indentation
        description_layout.addWidget(description_label)

        self.field_layout.addLayout(description_layout)


# Example usage
if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication, QVBoxLayout, QMainWindow

    class MainWindow(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Collapsible Task Example")

            central_widget = QWidget()
            layout = QVBoxLayout(central_widget)

            task1 = TaskWidget("Task 1", "This is the description of Task 1.")
            task2 = TaskWidget("Task 2", "This is another description.")

            layout.addWidget(task1)
            layout.addWidget(task2)
            layout.addStretch()

            self.setCentralWidget(central_widget)
            self.resize(400, 300)

    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
