# imports
import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from pathlib import Path
import socket
from random import randrange

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def runApp():
        from mainwindow import MainWindow
        window = MainWindow()
        app.exec_()

if __name__ == '__main__':
    # run the app
    try:
        app = QApplication(sys.argv)
        app.setApplicationName(".bullet")
        app.setWindowIcon(QIcon('logo.png'))
        sys.exit(runApp())
    except Exception as e:
        print(e)
    finally:
        sys.exit(0)