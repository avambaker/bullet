# imports
import sys
import logging

from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from pyupdater.client import Client
from pathlib import Path

from src.controllers.dbcontroller import db_controller
from src.controllers.pathcontroller import resource_path
from src.windows.mainwindow import MainWindow

def runApp():
        window = MainWindow()
        app.exec_()

def check_for_updates():
    client = Client('bullet', Path.home() / '.pyupdater')
    client.refresh()
    app_update = client.update_check('bullet', '1.0.0')  # Replace with your version
    if app_update:
        app_update.download()
        if app_update.is_downloaded():
            app_update.extract_restart()

if __name__ == '__main__':
    # run the app
    check_for_updates
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