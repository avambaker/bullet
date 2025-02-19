# imports
import sys
import os
import logging

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon

from src.controllers.dbcontroller import db_controller

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def runApp():
        from src.windows.mainwindow import MainWindow
        window = MainWindow()
        app.exec_()

if __name__ == '__main__':
    # run the app
    try:
        app = QApplication(sys.argv)
        app.setApplicationName(".bullet")
        app.setWindowIcon(QIcon('assets/bullet_logo.png'))
        sys.exit(runApp())
    except Exception as e:
        logging.exception("An error occurred: %s", e)
    finally:
        db_controller.close_connection()
        sys.exit(0)