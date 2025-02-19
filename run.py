# imports
import sys
import os
import logging

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon

from src.controllers.dbcontroller import db_controller
from src.controllers.pathcontroller import resource_path

def runApp():
        from src.windows.mainwindow import MainWindow
        window = MainWindow()
        app.exec_()

if __name__ == '__main__':
    # run the app
    try:
        app = QApplication(sys.argv)
        app.setApplicationName("bullet")
        app.setWindowIcon(QIcon(resource_path('assets/bullet_logo.icns')))
        sys.exit(runApp())
    except Exception as e:
        logging.exception("An error occurred: %s", e)
    finally:
        db_controller.close_connection()
        sys.exit(0)