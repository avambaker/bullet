
# imports
import os, sys, traceback
import sqlite3

from PyQt5.QtCore import Qt, QSortFilterProxyModel, QModelIndex
from PyQt5.QtWidgets import QMainWindow, QCheckBox, QToolButton, QWidget, QHBoxLayout, QFileDialog, QVBoxLayout, QLabel, QToolBar, QMessageBox, QHeaderView, QAction, QActionGroup, QMenu, QInputDialog, QTableView, QLineEdit
from PyQt5.QtGui import QCursor, QIcon
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
import pandas as pd
from datetime import date, datetime
from pathlib import Path
import json

class MainWindow(QMainWindow):
    def __init__(self):
        """Build window with task table"""
        super().__init__()
        # set up window
        self.setWindowTitle(".bullet")
        from run import resource_path

        # connect to database
        from dbcontroller import DatabaseController
        self.db_controller = DatabaseController()
        self.db_controller.connect_to_database()

        # Connect the table view to the model
        self.model = QSqlTableModel(self)
        self.model.setTable('projects') # Set the name of the table from the database
        if not self.model.select():
            print("Model select error:", self.model.lastError().text())
        if self.model.rowCount() == 0:
            print("No data found or unable to fetch data.")
        self.model.select()  # Fetch the data

        # create a proxy filter
        self.proxy = QSortFilterProxyModel()
        self.proxy.setSourceModel(self.model)
        self.proxy.setFilterKeyColumn(-1) # set the column to filter by as all
        self.proxy.setFilterCaseSensitivity(False)

        # create view model
        self.view = QTableView()
        self.view.verticalHeader().hide() # don't show indexes
        self.view.setSortingEnabled(True)
        self.view.setTextElideMode(Qt.ElideRight)
        self.view.setWordWrap(True)
        # Stretch the horizontal headers to fill the available space
        self.view.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.view.setModel(self.proxy)

        # create menu bar widgets
        new_action = QAction("New", self)
        view_action = QAction("View", self)
        settings_action = QAction("Settings", self)
        search_label = QLabel("Search: ")
        self.search_bar = QLineEdit()

        # add actions and widgets to a menu bar
        menubar = QToolBar()
        for action in [new_action, view_action, settings_action]:
            menubar.addAction(action)
        for widget in [search_label, self.search_bar]:
            menubar.addWidget(widget)
        
        # connect the search bar to the proxy model
        self.search_bar.textChanged.connect(self.proxy.setFilterFixedString)

        # vertically stack search bar with menubar and view
        vbox = QVBoxLayout()
        vbox.addWidget(menubar)
        vbox.addWidget(self.view)
        vbox.setContentsMargins(0,0,0,0)

        # put layout in widget and place widget on window
        container = QWidget()
        container.setLayout(vbox)
        self.setCentralWidget(container)
        self.showMaximized()
    
    def refresh_data(self):
        self.model.select()

def contextMenuEvent(self, event):
    # Get the index of the row that was right-clicked
    view_index = self.view.indexAt(event.pos())
    
    # Map this index to the proxy model
    proxy_index = self.proxy.mapToSource(view_index)
    
    # Check if the index is valid
    if not proxy_index.isValid():
        QMessageBox.critical(self, 'Error', 'The index clicked was invalid.')
        return
    
    # Retrieve the row and column information
    row = proxy_index.row()
    column = proxy_index.column()
    
    # Fetch the column name using the model's header data
    col_name = self.model.headerData(column, Qt.Horizontal)

    # Optionally, create and show a context menu
    menu = QMenu(self)
    open_action = menu.addAction("Open")
    
    # Connect actions to respective methods or slots
    open_action.triggered.connect(lambda: self.open_item(row))
    
    # Display the context menu at the cursor position
    menu.exec_(event.globalPos())

def open_item(self, row):
    print(f"Open item at row {row}")
