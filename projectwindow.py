
# imports
import os, sys, traceback
import sqlite3

from PyQt5.QtCore import Qt, pyqtSignal, QModelIndex, QPoint, QSize
from PyQt5.QtWidgets import QMainWindow, QDialog, QSpacerItem, QSizePolicy, QWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout, QMessageBox, QHeaderView, QAction, QActionGroup, QMenu, QInputDialog, QTableView, QLineEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
import pandas as pd
from datetime import date, datetime
from pathlib import Path
import json

class ProjectWindow(QMainWindow):
    dataUpdated = pyqtSignal()

    def __init__(self, databasecontroller, id = None, parent=None):
        """Build window with task table"""
        super().__init__(parent)

        # save variables
        self.id = id
        self.db_controller = databasecontroller

        # get access to json
        from JSONHandler import json_handler
        styles = {"Description": json_handler.get_css("Description"),
                  "Main Deadline": json_handler.get_css("Main Deadline")}
        icon_button_style = json_handler.get_css("icon_button")

        # query data to set up page
        (_, self.title, self.description, self.deadline) = self.db_controller.execute_query("SELECT * FROM projects WHERE project_id = ?", [self.id])[0]
        from JSONHandler import json_handler
        self.fields = self.db_controller.execute_query(json_handler.get_function("get_fields_by_project"), (self.id,))
        self.tasks = self.db_controller.execute_query(json_handler.get_function("get_tasks_by_project"), (self.id,))
        self.widget_order = self.db_controller.execute_query(json_handler.get_function("get_widget_order_by_project"), (self.id,))

        # Menu bar
        menu_bar = self.menuBar()
        project_menu = menu_bar.addMenu("Project")
        rename_action = QAction("Rename", self)
        edit_description_action = QAction("Edit Description", self)
        edit_deadline_action = QAction("Edit Deadline", self)
        delete_deadline_action = QAction("Delete Deadline", self)
        delete_action = QAction("Delete Project", self)

        project_menu.addAction(rename_action)
        project_menu.addAction(edit_description_action)
        project_menu.addAction(edit_deadline_action)
        project_menu.addAction(delete_deadline_action)
        project_menu.addAction(delete_action)

        rename_action.triggered.connect(self.rename_project)
        edit_description_action.triggered.connect(self.edit_description)
        delete_deadline_action.triggered.connect(self.delete_deadline)
        edit_deadline_action.triggered.connect(self.edit_deadline)
        delete_action.triggered.connect(self.delete_project)

        # create a layout
        self.widgets_layout = QVBoxLayout() # create vertical layout
        self.widgets_layout.setSpacing(15)  # Sets the space between widgets
        self.widgets_layout.setContentsMargins(10, 10, 10, 10)  # Sets the margins around the layout

        # dynamically add each field
        field_index = 0
        task_index = 0
        for _, widget_type in self.widget_order:
            if widget_type == 'fields':
                try:
                    self.putFieldOnWindow(*self.fields[field_index])
                    field_index += 1
                except Exception as e:
                    print(f"Error adding field {self.fields[field_index]} to project {self.id}")
                    print(e)
            else:
                try:
                    self.putTaskOnWindow(*self.tasks[task_index])
                    task_index += 1
                except Exception as e:
                    print(f"Error adding task {self.tasks[task_index]} to project {self.id}")
                    print(e)
        
        # add a new field button
        add_button = QPushButton("")
        add_button.setIcon(QIcon("icons/plus.png"))
        add_button.setMinimumSize(QSize(45, 45))
        add_button.setIconSize(QSize(45, 45))
        add_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        add_button.setFlat(True)
        add_button.setStyleSheet(icon_button_style)
        add_button.clicked.connect(self.openFieldCreator)

        # create description label
        self.description_label = QLabel(self.description)
        self.description_label.setStyleSheet(styles["Description"])
        self.description_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.description_label.setWordWrap(True)

        # create deadline widget
        self.project_deadline_label = QLabel(self.deadline)
        self.project_deadline_label.setStyleSheet(styles["Main Deadline"])
        self.project_deadline_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.project_deadline_label.setWordWrap(True)

        # Create a layout for button area
        button_layout = QHBoxLayout()
        button_layout.addWidget(add_button)

        # create an overall layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.description_label)
        main_layout.addWidget(self.project_deadline_label)
        main_layout.addLayout(self.widgets_layout)
        main_layout.addLayout(button_layout)
        # add a spacer so widgets appear at the top
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # hide the deadline and description if empty
        if self.description == "":
            self.description_label.hide()
        if self.deadline == "":
            self.project_deadline_label.hide()

        # set layout in a container
        container = QWidget(self)
        container.setLayout(main_layout)

        # set up window
        self.setWindowTitle(self.title)
        self.setCentralWidget(container)
        self.setGeometry(100, 100, 800, 600)
        self.setMenuBar(menu_bar)
    
    def openFieldEditor(self, field_widget, field_id, field_type, field_content):
        from fieldedit import FieldEditor
        edit_window = FieldEditor(field_type, field_content)
        if edit_window.exec_():  # If user clicked Save
            new_value = edit_window.new_val
            if new_value is not None and new_value != field_content:
                self.db_controller.execute_query("UPDATE fields SET content = ? WHERE field_id = ?", [new_value, field_id])
                field_widget.setText(new_value)
    
    def openFieldCreator(self):
        from widgetcreate import WidgetCreator
        create_window = WidgetCreator()
        if create_window.exec_():
            if create_window.w_type != "" and create_window.w_content != "":
                # if the new widget is a field
                if create_window.w_type == 'Header' or create_window.w_type == 'Paragraph':
                    widget_group = 'fields'
                    insert_query = "INSERT INTO fields (field_type, content) VALUES (?, ?)"
                    params = [create_window.w_type, create_window.w_content]
                    self.db_controller.execute_query(insert_query, params)
                    field_id_query = "SELECT MAX(field_id) FROM fields"
                    widget_id = self.db_controller.execute_query(field_id_query)[0][0]
                # if the new widget is a task
                else:
                    widget_group = 'tasks'
                    self.db_controller.execute_query("INSERT INTO tasks (title) VALUES (?)", [create_window.w_content])
                    widget_id = self.db_controller.execute_query("SELECT MAX(task_id) FROM tasks")[0][0]
                # add the new widget to project_widgets (connect it to this page)
                pw_query = "INSERT INTO project_widgets (widget_id, widget_type, project_id) VALUES (?, ?, ?)"
                pw_params = [widget_id, widget_group, self.id]
                self.db_controller.execute_query(pw_query, pw_params)
                if widget_group == 'fields':
                    self.putFieldOnWindow(widget_id, *params)
                    self.fields.append([widget_id, create_window.w_type, create_window.w_content])
                else:
                    self.putTaskOnWindow(widget_id, create_window.w_content, 0)
                    self.tasks.append([widget_id, create_window.w_content, 0, ""])
                self.widget_order.append([widget_id, widget_group])
    
    def putFieldOnWindow(self, field_id, field_type, content):
        from fieldwidget import FieldWidget
        field = FieldWidget(field_type, content)
        field.editClicked.connect(lambda *_, fw=field, fid=field_id, f=field_type, v=content: 
                            self.openFieldEditor(fw, fid, f, v))
        field.deleteClicked.connect(lambda *_, fw=field, fid=field_id: 
                            self.deleteField(fw, fid))
        self.widgets_layout.addWidget(field)
    
    def putTaskOnWindow(self, task_id, title, completed, deadline=None):
        from taskwidget import TaskWidget
        task_widget = TaskWidget(task_id, title, completed, deadline)
        self.widgets_layout.addWidget(task_widget)
    
    def deleteField(self, field, field_id):
        self.widgets_layout.removeWidget(field)
        field.deleteLater()
        self.db_controller.execute_query("DELETE FROM fields WHERE field_id = ?", [field_id])
        self.db_controller.execute_query("DELETE FROM project_widgets WHERE widget_id = ? AND widget_type = 'fields'", [field_id])
        # update self.fields and self.widget_order
        self.fields = [sublist for sublist in self.fields if sublist[0] != field_id]
        self.widget_order = [sublist for sublist in self.widget_order if sublist[0] != field_id and sublist[1] != 'fields']
        return
    
    def rename_project(self):
        from edit_dialog import EditDialog
        title_dialog = EditDialog(self.title, "Title", self.title, self)
        if title_dialog.exec_() == QDialog.Accepted:
            new_name = title_dialog.get_text()
            if new_name != "" and new_name != self.title:
                # Update the project title in the database
                self.db_controller.execute_query("UPDATE projects SET title = ? WHERE project_id = ?", [new_name, self.id])
                
                # Change the window's title to the new name
                self.setWindowTitle(new_name)
                self.title = new_name
                
                # Emit a signal to notify that the data has been updated
                self.dataUpdated.emit()
    
    def edit_description(self):
        from edit_dialog import EditDialog
        description_dialog = EditDialog(self.title, "Description", self.description, self)
        if description_dialog.exec_() == QDialog.Accepted:
            new_description = description_dialog.get_text()
            if new_description != self.description:
                # Update the project title in the database
                self.db_controller.execute_query("UPDATE projects SET description = ? WHERE project_id = ?", [new_description, self.id])
                
                # Change the window's description qlabel to the new description
                self.description_label.show()
                self.description_label.setText(new_description)
                self.description = new_description
                
                # Emit a signal to notify that the data has been updated
                self.dataUpdated.emit()
    
    def edit_deadline(self):
        from edit_dialog import EditDialog
        deadline_dialog = EditDialog(self.title, "Deadline", self.deadline, self)
        if deadline_dialog.exec_() == QDialog.Accepted:
            new_deadline = deadline_dialog.get_text()
            if new_deadline != self.deadline:
                # Update the project title in the database
                self.db_controller.execute_query("UPDATE projects SET deadline = ? WHERE project_id = ?", [new_deadline, self.id])
                
                # Change the window's description qlabel to the new description
                self.project_deadline_label.show()
                self.project_deadline_label.setText(new_deadline)
                self.deadline = new_deadline
                
                # Emit a signal to notify that the data has been updated
                self.dataUpdated.emit()
    
    def delete_deadline(self):
        reply = QMessageBox.question(self, f"Delete {self.title} Deadline", 
            "Are you sure you want to remove the deadline from this project?", 
            QMessageBox.Yes | QMessageBox.No, 
            QMessageBox.No)

        # Check the user's response
        if reply == QMessageBox.Yes:
            # Proceed with deleting the project
            self.db_controller.execute_query("UPDATE projects SET deadline = ? WHERE project_id = ?", ["", self.id])
            self.deadline = ""
            self.project_deadline_label.hide()
            self.dataUpdated.emit()
    
    def delete_project(self):
        reply = QMessageBox.question(self, f"Delete {self.title}", 
            "Are you sure you want to delete this project?", 
            QMessageBox.Yes | QMessageBox.No, 
            QMessageBox.No)

        # Check the user's response
        if reply == QMessageBox.Yes:
            # Proceed with deleting the project
            self.db_controller.execute_query("DELETE FROM projects WHERE project_id = ?", [self.id])
            self.dataUpdated.emit()
            self.close()