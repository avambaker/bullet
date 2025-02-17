from noteswindow import Ui_NotesWidget
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QWidget,
    QMessageBox,
)
from sqlalchemy import Column, Integer, String
from dbcontroller import db_controller

class Note(db_controller.Base):
    __tablename__ = "note"
    id = Column(Integer, primary_key=True)
    text = Column(String(1000), nullable=False)
    x = Column(Integer, nullable=False, default=0)
    y = Column(Integer, nullable=False, default=0)


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

        self.closeButton.pressed.connect(self.delete_window)
        #self.moreButton.pressed.connect(create_new_note)
        self.textEdit.textChanged.connect(self.save)

        # Flags to store dragged-dropped
        self._drag_active = False


    def load(self):
        self.move(self.obj.x, self.obj.y)
        self.textEdit.setHtml(self.obj.text)

    def save(self):
        self.obj.x = self.x()
        self.obj.y = self.y()
        self.obj.text = self.textEdit.toHtml()
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
