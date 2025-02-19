
# imports
import logging

from PyQt5.QtCore import Qt, QSortFilterProxyModel, QSize
from PyQt5.QtWidgets import (QMainWindow, QAbstractItemView, QWidget,
                             QVBoxLayout, QLabel, QToolBar, QMessageBox,
                             QHeaderView, QAction, QMenu, QInputDialog,
                             QTableView, QLineEdit)
from PyQt5.QtGui import QIcon
from PyQt5.QtSql import QSqlTableModel

from src.controllers.dbcontroller import db_controller
from src.windows.notewindow import Note
from src.windows.projectwindow import ProjectWindow
from src.windows.notewindow import NoteWidget

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
        db_controller.connect_to_database()
        db_controller.execute_query("PRAGMA foreign_keys = ON;")

        # Connect the table view to the model
        self.model = ReadOnlySqlTableModel(self)
        self.model.setTable('projects') # Set the name of the table from the database
        if not self.model.select():
            logging.error(f"Model select error: {self.model.lastError().text()}")
        if self.model.rowCount() == 0:
            logging.warning("No data found or unable to fetch data.")
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
        new_action = QAction(QIcon("assets/icons/plus.png"), "New", self)
        new_action.triggered.connect(self.newProject)

        refresh_action = QAction(QIcon("assets/icons/database_refresh.png"), "Refresh", self)
        refresh_action.triggered.connect(self.refreshTable)

        note_action = QAction(QIcon("assets/icons/note.png"), "Create Note", self)
        note_action.triggered.connect(self.newNote)

        search_label = QLabel("Search: ")
        self.search_bar = QLineEdit(self)

        # set up toolbar
        toolbar = QToolBar()
        toolbar.setIconSize(QSize(13, 13))

        # add actions and widgets to a tool bar
        for action in [new_action, refresh_action, note_action]:
            toolbar.addAction(action)
        toolbar.addSeparator()
        for widget in [search_label, self.search_bar]:
            toolbar.addWidget(widget)
        
        # connect the search bar to the proxy model
        self.search_bar.textChanged.connect(self.proxy.setFilterFixedString)

        # vertically stack search bar with toolbar and view
        vbox = QVBoxLayout()
        vbox.addWidget(toolbar)
        vbox.addWidget(self.view)
        vbox.setContentsMargins(0,0,0,0)
        vbox.setSpacing(0)

        # put layout in widget and place widget on window
        container = QWidget()
        container.setLayout(vbox)
        self.setCentralWidget(container)
        self.model.layoutChanged.emit()

        # create menu bar
        menu = self.menuBar()
        view_menu = menu.addMenu("View")
        settings_menu = menu.addMenu("Settings")

        self.showMaximized()

        # load notes
        self.notes = []
        for note in db_controller.session.query(Note).all():
            self.newNote(note)

    
    def refreshTable(self):
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
        open_action.triggered.connect(lambda: self.openProjectWindow(id.data()))

        # Display the context menu at the cursor position
        menu.exec_(event.globalPos())

    def openProjectWindow(self, project_id):
        # Instantiate ProjectWindow and pass project_id and db_controller
        self.project_window = ProjectWindow(project_id)
        self.project_window.dataUpdated.connect(self.refreshTable)
        self.project_window.show()
    
    def newProject(self):
        project_name, input = QInputDialog.getText(None, "New Project", "Project Title:")
        if input and project_name != "":
            db_controller.execute_query("INSERT INTO projects (title) VALUES (?)", [project_name])
            self.refreshTable()
    
    def newNote(self, note=None):
        self.notes.append(NoteWidget(note))