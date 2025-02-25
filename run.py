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

logging.basicConfig(
    level=logging.DEBUG if not getattr(sys, 'frozen', False) else logging.INFO,  # Debug mode for development, Info for packaged
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler()  # Print logs to console
    ],
)
logger = logging.getLogger(__name__)

def runApp():
        window = MainWindow()
        app.exec_()

def check_for_updates():
    logger.info("Checking for updates...")
    client = Client('bullet')
    client.refresh()
    app_update = client.update_check('bullet', '1.0.0')  # Replace with your version
    if app_update:
        logger.info("Update available! Downloading...")
        app_update.download()
        if app_update.is_downloaded():
            logger.info("Update downloaded. Extracting and restarting...")
            app_update.extract_restart()
        else:
             logger.info("No update available.")

if __name__ == '__main__':
    # run the app
    try:
         check_for_updates()
    except Exception as e:
         logger.error(e)
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