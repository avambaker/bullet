from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QCheckBox, QPushButton, QMenu, QAction, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, pyqtSignal
import os
import sys

class TaskWidget(QWidget):
    taskChecked = pyqtSignal()  # Custom signal for edit action

    def __init__(self, databasecontroller, id, title, completed, deadline="", parent=None):
        super().__init__(parent)

        self.id = id
        self.deadline = deadline
        self.db_controller = databasecontroller
        
        from JSONHandler import json_handler
        self.styles = {"Task Title": json_handler.get_css("Task Title"),
                  "Task Header": json_handler.get_css("Task Header"),
                  "Task Paragraph": json_handler.get_css("Task Paragraph"),
                  "Task Widget": json_handler.get_css("Task Widget"),
                  "Task Deadline": json_handler.get_css("Task Deadline")}

        try:
            self.get_fields = json_handler.get_function("get_widgets_by_task")
        except Exception as e:
            print("error at declaration of self.get_fields:", e)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            print(exc_type, fname, exc_tb.tb_lineno)


        # Main Layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setSpacing(0)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        # Row Layout (Checkbox + Title)
        self.row_widget = QWidget()
        self.row_layout = QHBoxLayout(self.row_widget)
        self.row_layout.setContentsMargins(5, 5, 5, 5)
        
        self.checkbox = QCheckBox()
        if completed == 1:
            self.checkbox.setChecked(True)
        self.checkbox.pressed.connect(self.taskChecked.emit)
        self.title_label = QLabel(title) # change this later
        self.title_label.setStyleSheet(self.styles['Task Title'])
        
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
        self.collapsible_area = QWidget()
        self.collapsible_area.setStyleSheet(self.styles["Task Widget"])
        self.collapsible_area.setVisible(False)
        self.main_layout.addWidget(self.collapsible_area)

        # create layout
        self.field_layout = QVBoxLayout()
        self.collapsible_layout = QVBoxLayout()
        self.collapsible_layout.addLayout(self.field_layout)
        self.collapsible_area.setLayout(self.collapsible_layout)


        self.setStyleSheet(self.styles["Task Widget"])

        # add fields dynamically
        for (_, field_type, content) in self.db_controller.execute_query(self.get_fields, [self.id]):
            self.add_field(field_type, content)

        # create context menu
        self.context_menu = QMenu(self)

        # Add actions
        self.edit_action = QAction("Edit Task", self)
        self.delete_action = QAction("Delete Task", self)

        self.edit_action.triggered.connect(self.edit)
        self.delete_action.triggered.connect(self.delete)

        self.context_menu.addAction(self.edit_action)
        self.context_menu.addAction(self.delete_action)

        # create deadline
        if self.deadline:
            deadline_label = QLabel("Due: " + self.deadline)
        else:
            deadline_label = QLabel("No Deadline")
        self.collapsible_layout.addWidget(deadline_label, alignment=Qt.AlignRight)
        if not self.deadline:
            deadline_label.hide()

    def toggle_description(self):
        """Toggles the visibility of the description."""
        self.collapsible_area.setVisible(self.collapsible_area.isHidden())
        self.toggle_button.setText("▲" if not self.collapsible_area.isHidden() else "▼")

    def toggle_on_click(self, event):
        self.toggle_button.toggle()
        self.toggle_description()
    
    def add_field(self, field_type, content):
        description_layout = QHBoxLayout()
        description_layout.setContentsMargins(0, 0, 0, 0)

        spacer_widget = QWidget()
        spacer_widget.setFixedWidth(self.spacer_width)  # Match title width

        description_label = QLabel(content)
        description_label.setWordWrap(True)
        description_label.setStyleSheet(self.styles[f'Task {field_type}'])

        description_layout.addWidget(spacer_widget)  # Indentation
        description_layout.addWidget(description_label)

        self.field_layout.addLayout(description_layout)
    
    def contextMenuEvent(self, event):
        self.context_menu.exec_(event.globalPos())
    
    def edit(self):
        print("edit")
    
    def delete(self):
        reply = QMessageBox.question(self, f"Delete Task", 
            "Are you sure you want to delete this task?", 
            QMessageBox.Yes | QMessageBox.No, 
            QMessageBox.No)

        # Check the user's response
        if reply == QMessageBox.Yes:
            # Proceed with deleting the project
            from JSONHandler import json_handler
            self.db_controller.execute_query(json_handler.get_function("delete_task"), [self.id])
            self.deleteLater()