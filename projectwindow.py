
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
        self.header_style = json_handler.get_css("Header")
        self.paragraph_style = json_handler.get_css("Paragraph")
        icon_button_style = json_handler.get_css("icon_button")

        # query data to set up page
        fields = self.db_controller.execute_query(f"SELECT * FROM project_fields WHERE project_id = {self.id} ORDER BY field_id ASC")
        title = self.db_controller.execute_query(f"SELECT title FROM projects WHERE project_id = {self.id}")[0][0]

        # create a layout
        self.vbox = QVBoxLayout() # create vertical layout
        self.vbox.setSpacing(10)  # Sets the space between widgets
        self.vbox.setContentsMargins(10, 10, 10, 10)  # Sets the margins around the layout

         # dynamically add each field
        for (_, _, field_type, content) in fields:
            if field_type == 'Header':
                self.new_header(content)
            elif field_type == 'Paragraph':
                self.new_paragraph(content)
        
        # add a new field button
        add_button = QPushButton("") # Set the icon (using a plus icon from Qt)
        add_button.setIcon(QIcon("plus_button.png"))
        add_button.setMinimumSize(QSize(45, 45))
        add_button.setIconSize(QSize(45, 45))
        add_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        add_button.setStyleSheet(icon_button_style)
        add_button.clicked.connect(self.new_field)
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
    
    def new_header(self, content):
        header = QLabel(content)
        header.setStyleSheet("""
            QLabel {
                font-family: Arial;
                font-size: 40px;
                font-weight: bold;
                color: blue;
            }
        """)
        self.vbox.addWidget(header)
    
    def new_paragraph(self, content):
        paragraph = QLabel(content)
        paragraph.setStyleSheet(self.paragraph_style)
        paragraph.setWordWrap(True)
        self.vbox.addWidget(paragraph)
    
    def new_field(self):
        from fieldedit import FieldEditor
        self.edit_window = FieldEditor()
        self.edit_window.show()
