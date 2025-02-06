
# imports
import os, sys, traceback
import sqlite3

from PyQt5.QtCore import Qt, QSortFilterProxyModel, QModelIndex, QPoint, QSize
from PyQt5.QtWidgets import QMainWindow, QSpacerItem, QSizePolicy, QWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout, QMessageBox, QHeaderView, QAction, QActionGroup, QMenu, QInputDialog, QTableView, QLineEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
import pandas as pd
from datetime import date, datetime
from pathlib import Path
import json

class ProjectWindow(QMainWindow):
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
        fields = self.db_controller.execute_query("SELECT * FROM project_fields WHERE project_id = ? ORDER BY field_id ASC", [self.id])
        (_, title, description, deadline) = self.db_controller.execute_query("SELECT * FROM projects WHERE project_id = ?", [self.id])[0]

        # create a layout
        self.fields_layout = QVBoxLayout() # create vertical layout
        self.fields_layout.setSpacing(15)  # Sets the space between widgets
        self.fields_layout.setContentsMargins(10, 10, 10, 10)  # Sets the margins around the layout

        # dynamically add each field
        from fieldwidget import FieldWidget
        for (field_id, project_id, field_type, content) in fields:
            self.putFieldOnWindow(field_id, project_id, field_type, content)
        
        # add a new field button
        add_button = QPushButton("")
        add_button.setIcon(QIcon("icons/plus.png"))
        add_button.setMinimumSize(QSize(45, 45))
        add_button.setIconSize(QSize(45, 45))
        add_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        add_button.setFlat(True)
        add_button.setStyleSheet(icon_button_style)
        add_button.clicked.connect(lambda: self.openFieldCreator())

        # create description label
        description_label = QLabel(description)
        description_label.setStyleSheet(styles["Description"])
        description_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        description_label.setWordWrap(True)

        # create deadline widget
        project_deadline_label = QLabel(deadline)
        project_deadline_label.setStyleSheet(styles["Main Deadline"])
        project_deadline_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        project_deadline_label.setWordWrap(True)

        # Create a layout for button area
        button_layout = QHBoxLayout()
        button_layout.addWidget(add_button)

        # create an overall layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(description_label)
        main_layout.addWidget(project_deadline_label)
        main_layout.addLayout(self.fields_layout)
        main_layout.addLayout(button_layout)
        # add a spacer so widgets appear at the top
        main_layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # set layout in a container
        container = QWidget(self)
        container.setLayout(main_layout)

        # set up window
        self.setWindowTitle(title)
        self.setCentralWidget(container)
        self.setGeometry(100, 100, 800, 600)
    
    def openFieldEditor(self, field_widget, field_id, project_id, field_type, field_content):
        from fieldedit import FieldEditor
        edit_window = FieldEditor(field_type, field_content)
        if edit_window.exec_():  # If user clicked Save
            new_value = edit_window.new_val
            if new_value is not None and new_value != field_content:
                self.db_controller.execute_query("UPDATE project_fields SET content = ? WHERE field_id = ? AND project_id = ?", [new_value, field_id, project_id])
                field_widget.setText(new_value)
    
    def openFieldCreator(self):
        from fieldcreate import FieldCreator
        create_window = FieldCreator()
        if create_window.exec_():
            if create_window.f_type != "" and create_window.f_content != "":
                insert_query = "INSERT INTO project_fields (project_id, field_type, content) VALUES (?, ?, ?)"
                params = [self.id, create_window.f_type, create_window.f_content]
                self.db_controller.execute_query(insert_query, params)
                field_id_query = "SELECT field_id FROM project_fields WHERE project_id = ? AND field_type = ? AND content = ?"
                field_id = self.db_controller.execute_query(field_id_query, params)[0][0]
                self.putFieldOnWindow(field_id, *params)
    
    def putFieldOnWindow(self, field_id, project_id, field_type, content):
        from fieldwidget import FieldWidget
        field = FieldWidget(field_type, content)
        field.editClicked.connect(lambda *_, fw=field, fid=field_id, pid=project_id, f=field_type, v=content: 
                            self.openFieldEditor(fw, fid, pid, f, v))
        field.deleteClicked.connect(lambda *_, fw=field, fid=field_id, pid=project_id: 
                            self.deleteField(fw, fid, pid))
        self.fields_layout.addWidget(field)
    
    def deleteField(self, field, field_id, project_id):
        self.fields_layout.removeWidget(field)
        field.deleteLater()
        query = "DELETE FROM project_fields WHERE field_id = ? AND project_id = ?"
        params = [field_id, project_id]
        self.db_controller.execute_query(query, params)
        return