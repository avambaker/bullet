
# imports
import os, sys, traceback
import sqlite3

from PyQt5.QtCore import Qt, QSortFilterProxyModel, QModelIndex, QPoint
from PyQt5.QtWidgets import QMainWindow, QAbstractItemView, QToolButton, QWidget, QHBoxLayout, QFileDialog, QVBoxLayout, QLabel, QToolBar, QMessageBox, QHeaderView, QAction, QActionGroup, QMenu, QInputDialog, QTableView, QLineEdit
from PyQt5.QtGui import QCursor, QIcon
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
import pandas as pd
from datetime import date, datetime
from pathlib import Path
import json

class ReadOnlySqlTableModel(QSqlTableModel):
    def flags(self, index):
        flags = super().flags(index)
        return flags & ~Qt.ItemIsEditable

class MainWindow(QMainWindow):
    def __init__(self):
        """Build window with task table"""
        super().__init__()
        # set up window
        self.setWindowTitle(".bullet")

        # connect to database
        from dbcontroller import DatabaseController
        self.db_controller = DatabaseController()
        self.db_controller.connect_to_database()

        # Connect the table view to the model
        self.model = ReadOnlySqlTableModel(self)
        self.model.setTable('projects') # Set the name of the table from the database
        if not self.model.select():
            print("Model select error:", self.model.lastError().text())
        if self.model.rowCount() == 0:
            print("No data found or unable to fetch data.")
        self.model.select()  # Fetch the data
        self.model.setEditStrategy(QSqlTableModel.OnManualSubmit)

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
        self.view.setSelectionMode(QAbstractItemView.NoSelection)
        self.view.setModel(self.proxy)
        self.view.setContentsMargins(0, 0, 0, 0)  # Remove margins
        self.view.hideColumn(0) # hide the project id's

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
        vbox.setSpacing(0)

        # put layout in widget and place widget on window
        container = QWidget()
        container.setLayout(vbox)
        self.setCentralWidget(container)
        self.model.layoutChanged.emit()
        self.showMaximized()
    
    def refresh_data(self):
        self.model.select()

    def contextMenuEvent(self, event):
       # get row clicked on
        view_index = self.view.selectionModel().currentIndex()
        # map row to proxy
        proxy_index = self.proxy.index(view_index.row(), view_index.column())
        # check validity of proxy index
        if not proxy_index.isValid():
            QMessageBox.critical(None, 'Error', 'The index clicked was invalid.')
            return
        # map row to model
        model_qindex = self.proxy.mapToSource(proxy_index)
        # check validity of model index
        if not model_qindex.isValid():
            QMessageBox.critical(None, 'Error', 'The index clicked was invalid.')
            return

        # get row index and column name
        row = model_qindex.row()
        id = self.model.index(row, 0)

        # Optionally, create and show a context menu
        menu = QMenu(self)
        open_action = menu.addAction("Open")

        # Use a lambda function to pass arguments to the slot
        open_action.triggered.connect(lambda: self.open_project_window(id.data()))

        # Display the context menu at the cursor position
        menu.exec_(event.globalPos())

    def open_project_window(self, project_id):
        from projectwindow import ProjectWindow
        # Instantiate ProjectWindow and pass project_id and db_controller
        self.project_window = ProjectWindow(self.db_controller, project_id)
        self.project_window.show()