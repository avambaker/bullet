
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
        styles = {"Header": json_handler.get_css("Header"),
                  "Paragraph": json_handler.get_css("Paragraph")}
        icon_button_style = json_handler.get_css("icon_button")

        # query data to set up page
        fields = self.db_controller.execute_query("SELECT * FROM project_fields WHERE project_id = ? ORDER BY field_id ASC", [self.id])
        title = self.db_controller.execute_query("SELECT title FROM projects WHERE project_id = ?", [self.id])[0][0]

        # create a layout
        self.vbox = QVBoxLayout() # create vertical layout
        self.vbox.setSpacing(10)  # Sets the space between widgets
        self.vbox.setContentsMargins(10, 10, 10, 10)  # Sets the margins around the layout

        # dynamically add each field
        from fieldwidget import FieldWidget
        for (field_id, project_id, field_type, content) in fields:
            field = FieldWidget(field_type, content)
            field.editClicked.connect(lambda *_, fw=field, fid=field_id, pid=project_id, f=field_type, v=content: 
                              self.open_field_editor(fw, fid, pid, f, v))
            #field.editClicked.connect(lambda *_, fid = field_id, pid = project_id, f=field_type, v=content: self.open_field_editor(fid, pid, f, v))
            self.vbox.addWidget(field)
        
        # add a new field button
        add_button = QPushButton("")
        add_button.setIcon(QIcon("plus_button.png"))
        add_button.setMinimumSize(QSize(45, 45))
        add_button.setIconSize(QSize(45, 45))
        add_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        add_button.setFlat(True)
        add_button.setStyleSheet(icon_button_style)
        add_button.clicked.connect(lambda: self.open_field_editor("", ""))
        # Create a layout for the button
        hbox = QHBoxLayout()
        #hbox.addStretch(1)  # Add stretchable space before the button
        hbox.addWidget(add_button)
        #hbox.addStretch(1)
        self.vbox.addLayout(hbox)
        
        # add a spacer so widgets appear at the top
        self.vbox.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # set layout in a container
        container = QWidget(self)
        container.setLayout(self.vbox)

        # set up window
        self.setWindowTitle(title)
        self.setCentralWidget(container)
        self.setGeometry(100, 100, 800, 600)
    
    def set_up_field(self, style, content):
        widget = QLabel(content)
        widget.setStyleSheet(style)
        widget.setWordWrap(True)

    def new_paragraph(self, content):
        paragraph = QLabel(content)
        paragraph.setStyleSheet(self.paragraph_style)
        paragraph.setWordWrap(True)
        # Create a horizontal layout for the label and button
        header_layout = QHBoxLayout()
        header_layout.addWidget(paragraph)
        header_layout.addWidget(self.edit_button)
        header_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins
        header_layout.setSpacing(5)  # Set spacing between label and button

        self.vbox.addWidget(paragraph)
    
    def open_field_editor(self, field_widget, field_id, project_id, field_type, field_content):
        from fieldedit import FieldEditor
        edit_window = FieldEditor(field_type, field_content)
        if edit_window.exec_():  # If user clicked Save
            new_value = edit_window.new_val
            if new_value is not None and new_value != field_content:
                self.db_controller.execute_query("UPDATE project_fields SET content = ? WHERE field_id = ? AND project_id = ?", [new_value, field_id, project_id])
                field_widget.setText(new_value)
    
    def open_field_creator(self):
        from fieldcreate import FieldCreator
        self.create_window = FieldCreator()
        self.create_window.show()