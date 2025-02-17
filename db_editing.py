import sqlite3
import sys
# importing libraries
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from datetime import datetime, timedelta

# Connect to the SQLite database
conn = sqlite3.connect('notes.db')
cursor = conn.cursor()

#str_date = date.strftime("%a %m/%d/%Y %I:%M %p")

queries = []

for i, query in enumerate(queries):
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        for row in results:
            print(row)
    except Exception as e:
        print("ERROR WITH QUERY #", i+1)
        print(e)

# Commit the changes and close the connection
conn.commit()
conn.close()
print("done")

query = """
SELECT record_index
FROM (SELECT  pwidget_id, ROW_NUMBER() OVER (ORDER BY display_order) - 1 AS record_index
FROM project_widgets
WHERE project_id = ?
ORDER BY display_order ASC)
WHERE pwidget_id = ?;
"""

def add_to_json(query, query_name):
    import json
    with open("sqlite_functions.json", "r") as f:
        data = json.load(f)
    data[query_name] = query
    with open("sqlite_functions.json", "w") as json_file:
        json.dump(data, json_file, indent=4)
    print("succesfully edited json")

#add_to_json(query, "get_layout_location_of_widget")