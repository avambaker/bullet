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
#cursor.execute("UPDATE projects SET deadline = ? WHERE project_id = 3", (str_date,))
queries = ["""
CREATE TABLE project_order (
    project_id INTEGER NOT NULL,
    item_type TEXT CHECK (item_type IN ('field', 'task')),
    item_id INTEGER NOT NULL,
    display_order INTEGER NOT NULL,
    PRIMARY KEY (project_id, item_type, item_id),
    FOREIGN KEY (project_id) REFERENCES projects(project_id) ON DELETE CASCADE
);""",

"""
CREATE TRIGGER ensure_project_order_for_fields
BEFORE INSERT ON project_order
WHEN NEW.item_type = 'field'
AND NOT EXISTS (SELECT 1 FROM project_fields WHERE field_id = NEW.item_id AND project_id = NEW.project_id)
BEGIN
    SELECT RAISE(ABORT, 'Invalid item_id: No matching field_id in project_fields');
END;""",

"""
CREATE TRIGGER ensure_project_order_for_tasks
BEFORE INSERT ON project_order
WHEN NEW.item_type = 'task'
AND NOT EXISTS (SELECT 1 FROM subtasks WHERE task_id = NEW.item_id AND project_id = NEW.project_id)
BEGIN
    SELECT RAISE(ABORT, 'Invalid item_id: No matching task_id in subtasks');
END;
"""]
for query in queries:
    cursor.execute(query)

# Commit the changes and close the connection
conn.commit()
conn.close()
