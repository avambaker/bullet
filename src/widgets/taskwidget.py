import logging

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QCheckBox, QPushButton, QMenu,
                             QAction, QMessageBox, QTextEdit, QLineEdit,
                             QDialog, QDialogButtonBox, QFormLayout,
                             QDateTimeEdit)
from PyQt5.QtCore import Qt, pyqtSignal, QDateTime
from datetime import datetime
from src.controllers.dbcontroller import db_controller
from src.controllers.JSONcontroller import json_handler

class TaskWidget(QWidget):
    taskChecked = pyqtSignal()  # Custom signal for edit action
    moveTaskUp = pyqtSignal()
    moveTaskDown = pyqtSignal()

    def __init__(self, id, title, completed, body = "", deadline="", parent=None):
        super().__init__(parent)

        self.id = id
        self.deadline = deadline
        self.body = body
        self.title = title
        
        self.styles = {"Task Title": json_handler.get_css("Task Title"),
                  "Task Header": json_handler.get_css("Task Header"),
                  "Task Paragraph": json_handler.get_css("Task Paragraph"),
                  "Task Widget": json_handler.get_css("Task Widget"),
                  "Task Deadline": json_handler.get_css("Task Deadline")}

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
        body_layout = QHBoxLayout()
        self.collapsible_layout = QVBoxLayout()
        self.collapsible_layout.addLayout(body_layout)
        self.collapsible_area.setLayout(self.collapsible_layout)


        self.setStyleSheet(self.styles["Task Widget"])

        # add fields dynamically
        body_layout.setContentsMargins(0, 0, 0, 0)

        spacer_widget = QWidget()
        spacer_widget.setFixedWidth(self.spacer_width)  # Match title width

        self.body_label = QLabel(self.body)
        self.body_label.setWordWrap(True)
        self.body_label.setStyleSheet(self.styles['Task Paragraph'])

        body_layout.addWidget(spacer_widget)  # Indentation
        body_layout.addWidget(self.body_label)

        # create context menu
        self.context_menu = QMenu(self)

        # Add actions
        self.edit_action = QAction("Edit Task", self)
        self.delete_action = QAction("Delete Task", self)
        self.move_up_action = QAction("Move Up", self)
        self.move_down_action = QAction("Move Down", self)

        self.edit_action.triggered.connect(self.edit)
        self.delete_action.triggered.connect(self.delete)
        self.move_up_action.triggered.connect(self.moveTaskUp.emit)
        self.move_down_action.triggered.connect(self.moveTaskDown.emit)

        self.context_menu.addAction(self.edit_action)
        self.context_menu.addAction(self.delete_action)
        self.context_menu.addAction(self.move_up_action)
        self.context_menu.addAction(self.move_down_action)

        # create deadline
        if self.deadline:
            self.deadline_label = QLabel("Due: " + self.deadline)
        else:
            self.deadline_label = QLabel("No Deadline")
        self.collapsible_layout.addWidget(self.deadline_label, alignment=Qt.AlignRight)
        if not self.deadline:
            self.deadline_label.hide()

    def toggle_description(self):
        """Toggles the visibility of the description."""
        self.collapsible_area.setVisible(self.collapsible_area.isHidden())
        self.toggle_button.setText("▲" if not self.collapsible_area.isHidden() else "▼")

    def toggle_on_click(self, event):
        self.toggle_button.toggle()
        self.toggle_description()
    
    def contextMenuEvent(self, event):
        self.context_menu.exec_(event.globalPos())
    
    def edit(self):
        edit_dialog = QDialog()
        edit_dialog.setWindowTitle("Edit Task")
        edit_dialog.setGeometry(100, 100, 400, 300)

        # Create layout
        layout = QVBoxLayout()
        
        # Create a form layout for the input fields
        form_layout = QFormLayout()
        
        # Short form response 1
        title_input = QLineEdit()
        title_input.setText(self.title)
        form_layout.addRow(QLabel("Title:"), title_input)
        
        # Long form response
        body_input = QTextEdit()
        body_input.setPlainText(self.body)
        form_layout.addRow(QLabel("Body:"), body_input)
        
        # Short form response 2
        deadline_input = QDateTimeEdit()
        if self.deadline is not None and self.deadline != "":
            try:
                qdeadline = QDateTime(datetime.strptime(self.deadline, "%a %m/%d/%Y %I:%M %p"))
                deadline_input.setDateTime(qdeadline)
            except Exception as e:
                logging.error(f"Deadline {self.deadline} not valid on task {self.id}: {e}")
        form_layout.addRow(QLabel("Deadline:"), deadline_input)

        enable_deadline_input = QCheckBox()
        if self.deadline_label.isHidden():
            enable_deadline_input.setChecked(False)
        else:
            enable_deadline_input.setChecked(True)
        enable_deadline_input.stateChanged.connect(self.deadlineWarning)

        form_layout.addRow(QLabel("Enable Deadline:"), enable_deadline_input)
        
        # Dialog buttons
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(edit_dialog.accept)
        buttonBox.rejected.connect(edit_dialog.reject)
        
        # Add form layout and button box to the main layout
        layout.addLayout(form_layout)
        layout.addWidget(buttonBox)
        
        # Set the main layout
        edit_dialog.setLayout(layout)

        if edit_dialog.exec_() == QDialog.Accepted:
            new_title = title_input.text()
            new_body = body_input.toPlainText()
            if deadline_input.dateTime().isNull():
                new_deadline = ""
            else:
                new_deadline = deadline_input.dateTime().toString("ddd MM/dd/yyyy h:mm AP")
            if new_title != self.title:
                db_controller.execute_query(json_handler.get_function("update_title_in_task_data"), [new_title, self.id])
                self.title = new_title
                self.title_label.setText(self.title)
            if new_body != self.body:
                db_controller.execute_query(json_handler.get_function("update_body_in_task_data"), [new_body, self.id])
                self.body = new_body
                self.body_label.setText(self.body)
            if new_deadline != self.deadline and new_deadline != "Sat 01/01/2000 12:00 AM": # null deadline
                db_controller.execute_query(json_handler.get_function("update_deadline_in_task_data"), [new_deadline, self.id])
                self.deadline = new_deadline
                self.deadline_label.setText(f"Due: {self.deadline}")
                self.deadline_label.show()
            if enable_deadline_input.isChecked() and self.deadline is not None and self.deadline != "":
                self.deadline_label.show()
            if not enable_deadline_input.isChecked():
                self.deadline = ""
                db_controller.execute_query(json_handler.get_function("update_deadline_in_task_data"), ["", self.id])
                self.deadline_label.hide()
    
    def deadlineWarning(self, state):
        if state == Qt.Unchecked:
            QMessageBox.warning(self, "Disable Deadline", "Disabling the deadline will set it to null.")

    
    def delete(self):
        reply = QMessageBox.question(self, f"Delete Task", 
            "Are you sure you want to delete this task?", 
            QMessageBox.Yes | QMessageBox.No, 
            QMessageBox.No)

        # Check the user's response
        if reply == QMessageBox.Yes:
            # Proceed with deleting the project
            db_controller.execute_query(json_handler.get_function("delete_task"), [self.id])
            self.deleteLater()