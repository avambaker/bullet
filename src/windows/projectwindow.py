# imports
import os
import sys
import logging

from PyQt5.QtCore import pyqtSignal, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QMainWindow, QDialog, QSpacerItem, QSizePolicy, QScrollArea, 
    QWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout, 
    QMessageBox, QAction
)

from src.controllers.dbcontroller import db_controller
from src.controllers.JSONcontroller import json_handler
from src.controllers.pathcontroller import resource_path
from src.dialogs.fieldedit import FieldEditor
from src.dialogs.widgetcreate import WidgetCreator
from src.widgets.fieldwidget import FieldWidget
from src.dialogs.projectedit import ProjectEditor
from src.widgets.taskwidget import TaskWidget

class ProjectWindow(QMainWindow):
    dataUpdated = pyqtSignal()

    def __init__(self, id = None, parent=None):
        """Build window with task table"""
        super().__init__(parent)

        # save variables
        self.id = id

        # get access to json
        styles = {"Description": json_handler.get_css("Description"),
                  "Main Deadline": json_handler.get_css("Main Deadline")}
        icon_button_style = json_handler.get_css("icon_button")

        # query data to set up page
        (_, self.title, self.description, self.deadline) = db_controller.execute_query(json_handler.get_function("get_project_by_id"), [self.id])[0]
        query = json_handler.get_function("get_widgets_by_project")
        assert query is not None, "SQL query not found in json_handler"
        self.widgets = db_controller.execute_query(query, [self.id])
        if not self.widgets:
            self.widgets = []
        self.task_data = db_controller.execute_query(json_handler.get_function("get_task_data_by_project"), (self.id,))
        if not self.task_data:
            self.task_data = []

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
        task_index = 0
        for (pw_id, widget_type, content, page_pos) in self.widgets:
            if widget_type != 'Task':
                try:
                    self.putFieldOnWindow(pw_id, widget_type, content)
                except Exception as e:
                    logging.error(f"Error adding widget {pw_id} to project {self.id}: {e}")
            else:
                try:
                    self.putTaskOnWindow(*self.task_data[task_index])
                    task_index += 1
                except Exception as e:
                    logging.error(f"Error adding task {self.task_data[task_index]} to project {self.id}: {e}")
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    logging.info(f"{exc_type}, {fname}, {exc_tb.tb_lineno}")

        
        # add a new field button
        add_button = QPushButton("")
        add_button.setIcon(QIcon(resource_path("assets/icons/plus.png")))
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
        widget_container = QWidget(self)
        widget_container.setLayout(main_layout)
        widget_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        container = QScrollArea(self)
        container.setWidgetResizable(True)
        container.setWidget(widget_container)

        # set up window
        self.setWindowTitle(self.title)
        self.setCentralWidget(container)
        self.setGeometry(100, 100, 800, 600)
        self.setMenuBar(menu_bar)
    
    def openFieldEditor(self, field_widget, field_id, field_type, field_content):
        edit_window = FieldEditor(field_type, field_content)
        if edit_window.exec_():  # If user clicked Save
            new_value = edit_window.new_val
            if new_value is not None and new_value != field_content:
                db_controller.execute_query(json_handler.get_function("update_pwidget_content_by_id"), [new_value, field_id])
                field_widget.setText(new_value)
    
    def openFieldCreator(self):
        create_window = WidgetCreator()
        if create_window.exec_():
            if create_window.w_type != "" and create_window.w_content != "":
                # add to the database
                params = [self.id, create_window.w_type, create_window.w_content]
                insert_func = json_handler.get_function("insert_into_project_widgets")
                db_controller.execute_query(insert_func, params)

                # get the new pwidget_id
                widget_id = db_controller.execute_query(json_handler.get_function("get_max_pwidget_id"))[0][0]

                # add widget to the project page
                if create_window.w_type == 'Task':
                    self.putTaskOnWindow(widget_id, create_window.w_content)
                else:
                    self.putFieldOnWindow(widget_id, *params[1:])
    
    def putFieldOnWindow(self, field_id, field_type, content):
        field = FieldWidget(field_id, field_type, content)
        field.editClicked.connect(lambda *_, fw=field, fid=field_id, f=field_type, v=content: 
                            self.openFieldEditor(fw, fid, f, v))
        field.deleteClicked.connect(lambda *_, fw=field, fid=field_id: 
                            self.deleteField(fw, fid))
        field.moveUp.connect(lambda *_, fw=field: 
                            self.moveWidget(fw, -1))
        field.moveDown.connect(lambda *_, fw=field: 
                            self.moveWidget(fw, 1))
        self.widgets_layout.addWidget(field)
    
    def putTaskOnWindow(self, task_id, title, completed=0, content=None, deadline=None):
        task_widget = TaskWidget(task_id, title, completed, content, deadline)
        task_widget.taskChecked.connect(lambda *_: 
            self.updateTaskStatus(task_id, task_widget.checkbox.isChecked()))
        task_widget.moveTaskUp.connect(lambda *_, tw=task_widget: 
                            self.moveWidget(tw, -1))
        task_widget.moveTaskDown.connect(lambda *_, tw=task_widget: 
                            self.moveWidget(tw, 1))
        self.widgets_layout.addWidget(task_widget)
    
    def deleteField(self, field, field_id):
        self.widgets_layout.removeWidget(field)
        field.deleteLater()
        db_controller.execute_query(json_handler.get_function("delete_project_widget_by_id"), [field_id])
    
    def rename_project(self):
        title_dialog = ProjectEditor(self.title, "Title", self.title, self)
        if title_dialog.exec_() == QDialog.Accepted:
            new_name = title_dialog.get_text()
            if new_name != "" and new_name != self.title:
                # Update the project title in the database
                db_controller.execute_query(json_handler.get_function("rename_project_by_id"), [new_name, self.id])
                
                # Change the window's title to the new name
                self.setWindowTitle(new_name)
                self.title = new_name
                
                # Emit a signal to notify that the data has been updated
                self.dataUpdated.emit()
    
    def edit_description(self):
        description_dialog = ProjectEditor(self.title, "Description", self.description, self)
        if description_dialog.exec_() == QDialog.Accepted:
            new_description = description_dialog.get_text()
            if new_description != self.description:
                # Update the project title in the database
                db_controller.execute_query(json_handler.get_function("update_project_description"), [new_description, self.id])
                
                # Change the window's description qlabel to the new description
                self.description_label.show()
                self.description_label.setText(new_description)
                self.description = new_description
                
                # Emit a signal to notify that the data has been updated
                self.dataUpdated.emit()
    
    def edit_deadline(self):
        deadline_dialog = ProjectEditor(self.title, "Deadline", self.deadline, self)
        if deadline_dialog.exec_() == QDialog.Accepted:
            new_deadline = deadline_dialog.get_text()
            if new_deadline != self.deadline:
                # Update the project title in the database
                db_controller.execute_query(json_handler.get_function("update_project_deadline"), [new_deadline, self.id])
                
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
            db_controller.execute_query(json_handler.get_function("update_project_deadline"), ["", self.id])
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
            db_controller.execute_query(json_handler.get_function("delete_project"), [self.id])
            self.dataUpdated.emit()
            self.close()
    
    def updateTaskStatus(self, task_id, status):
        new_val = 0
        if status == False:
            new_val = 1
        db_controller.execute_query(json_handler.get_function("update_task_completed"), [new_val, task_id])
    
    def moveWidget(self, widget, y):
        # get location on page
        get_page_loc_query = json_handler.get_function("get_layout_location_of_widget")
        page_loc = db_controller.execute_query(get_page_loc_query, [self.id, widget.id])[0][0]

        # check that the move is valid
        last_index = self.widgets_layout.count() - 1
        if (page_loc, y) != (0, -1) and (page_loc, y) != (last_index, 1):
            
            # get display order for self and widget above (as well as id)
            pid2 = widget.id
            do2 = db_controller.execute_query(json_handler.get_function("get_display_order_by_id"), [pid2])[0][0]
            if y == -1:
                (pid1, do1) = db_controller.execute_query(json_handler.get_function("get_widget_above"), [pid2, pid2])[0]
            if y == 1:
                (pid1, do1) = db_controller.execute_query(json_handler.get_function("get_widget_below"), [pid2, pid2])[0]

            # update database by swapping the display order of the two widgets
            reset_DO_query = json_handler.get_function("update_display_order")
            db_controller.execute_query(reset_DO_query, [do2, pid1])
            db_controller.execute_query(reset_DO_query, [do1, pid2])

            # reorder the widgets on page
            self.widgets_layout.removeWidget(widget)
            try: self.widgets_layout.insertWidget(page_loc + y, widget)
            except Exception as e:
                logging.exception(f"An error occurred: {e}")