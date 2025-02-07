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

#str_date = date.strftime("%a %m/%d/%Y %I:%M %p")

queries = ["""
    SELECT t.task_id, t.title, t.completed, t.deadline
    FROM project_widgets pw
    LEFT JOIN tasks t ON pw.widget_id = t.task_id
    WHERE pw.project_id = ? AND pw.widget_type = 'tasks'
    ORDER BY pw.display_order;
"""
]

for i, query in enumerate(queries):
    try:
        cursor.execute(query, (1,))
        results = cursor.fetchall()
        for row in results:
            print(row)
    except Exception as e:
        print("ERROR WITH QUERY #", i+1)
        print(e)

# Commit the changes and close the connection
conn.commit()
conn.close()

def add_to_json(query_dict):
    import json
    with open("sqlite_functions.json", "r") as f:
        data = json.load(f)
    data.update(query_dict)
    with open("sqlite_functions.json", "w") as json_file:
        json.dump(data, json_file, indent=4)
