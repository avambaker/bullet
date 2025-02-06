import sqlite3
import sys
# importing libraries
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from datetime import datetime, timedelta

# Connect to the SQLite database
conn = sqlite3.connect('data.db')
cursor = conn.cursor()

# Step 1: Create a new table with AUTOINCREMENT on field_id and a composite primary key
date = datetime.now() + timedelta(days=60)
str_date = date.strftime("%a %m/%d/%Y %I:%M %p")
print(str_date)
#cursor.execute("UPDATE projects SET deadline = ? WHERE project_id = 3", (str_date,))

# Commit the changes and close the connection
conn.commit()
conn.close()
