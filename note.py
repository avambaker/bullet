from noteswindow import Ui_NotesWidget
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget,
    QMessageBox,
    QColorDialog,
    QSizePolicy,
    QMenu,
    QAction
)
from sqlalchemy import Column, Integer, String
from dbcontroller import db_controller

class Note(db_controller.Base):
    __tablename__ = "note"
    id = Column(Integer, primary_key=True)
    text = Column(String(1000), nullable=False)
    x = Column(Integer, nullable=False, default=0)
    y = Column(Integer, nullable=False, default=0)
    background_color = Column(String(7), nullable=True)
    opacity = Column(Integer, default=0)

class NoteWidget(QWidget, Ui_NotesWidget):
    def __init__(self, obj=None):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlags(
            self.windowFlags()
            | Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
        )
        self.show()

        # Load/save note data, store this notes db reference.
        if obj:
            self.obj = obj
            self.load()
        else:
            self.obj = Note()
            self.save()

        self.textEdit.textChanged.connect(self.save)

        # Flags to store dragged-dropped
        self._drag_active = False

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        menu = QMenu()
        color_action = QAction("Change Color", self)
        visibility_action = QAction("Toggle Visibility", self)
        floating_action = QAction("Toggle Floating", self)
        delete_action = QAction("Delete Note", self)
        
        color_action.triggered.connect(self.changeColor)
        visibility_action.triggered.connect(self.toggleVisibility)
        floating_action.triggered.connect(self.toggleFloating)
        delete_action.triggered.connect(self.delete_window)

        menu.addAction(color_action)
        menu.addAction(visibility_action)
        menu.addAction(floating_action)
        menu.addAction(delete_action)

        self.menuButton.setMenu(menu)
        self.show()


    def load(self):
        self.move(self.obj.x, self.obj.y)
        self.textEdit.setHtml(self.obj.text)
        if self.obj.background_color:
            self.setStyleSheet(f"background-color: {self.obj.background_color};")
            self.textEdit.setStyleSheet(f"background-color: {self.obj.background_color};")
        if self.obj.opacity == 1:
            self.setWindowOpacity(0.6)

    def save(self):
        self.obj.x = self.x()
        self.obj.y = self.y()
        self.obj.text = self.textEdit.toHtml()
        self.obj.background_color = self.palette().color(self.backgroundRole()).name()
        if self.windowOpacity() == 1:
            self.obj.opacity = 0
        else:
            self.obj.opacity = 1
        db_controller.session.add(self.obj)
        db_controller.session.commit()

    def mousePressEvent(self, e):
        self.previous_pos = e.globalPos()

    def mouseMoveEvent(self, e):
        delta = e.globalPos() - self.previous_pos
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.previous_pos = e.globalPos()

        self._drag_active = True

    def mouseReleaseEvent(self, e):
        if self._drag_active:
            self.save()
            self._drag_active = False

    def delete_window(self):
        result = QMessageBox.question(
            self,
            "Confirm delete",
            "Are you sure you want to delete this note?",
        )
        if result == QMessageBox.StandardButton.Yes:
            db_controller.session.delete(self.obj)
            db_controller.session.commit()
            self.close()
    
    def changeColor(self):
        color = QColorDialog.getColor()
        if color.isValid():  # Ensure a valid color is chosen
            self.setStyleSheet(f"background-color: {color.name()};")
            self.textEdit.setStyleSheet(f"background-color: {color.name()};")
            self.save()
    
    def toggleVisibility(self):
        if self.windowOpacity() == 1:
            self.setWindowOpacity(0.6)
        else:
            self.setWindowOpacity(1)
        self.save()
    
    def toggleFloating(self):
        flags = self.windowFlags()
        if flags & Qt.WindowType.WindowStaysOnTopHint:
            new_flags = flags & ~Qt.WindowType.WindowStaysOnTopHint
        else:
            new_flags = flags | Qt.WindowType.WindowStaysOnTopHint
        self.setWindowFlags(new_flags)
        self.show()  # Required to apply changes