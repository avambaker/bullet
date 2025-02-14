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

temp = [
    """CREATE TABLE "project_widgets" (
	"pwidget_id"	INTEGER NOT NULL,
	"project_id"	INTEGER NOT NULL,
	"widget_type"	TEXT NOT NULL CHECK("widget_type" IN ("Header", "Paragraph", "Task")),
	"content"	TEXT NOT NULL,
	"display_order"	INTEGER,
	PRIMARY KEY("pwidget_id" AUTOINCREMENT),
	FOREIGN KEY("project_id") REFERENCES "projects"("project_id") ON DELETE CASCADE
);
""","""

CREATE TABLE "task_data" (
	"pwidget_id"	INTEGER,
	"title"	TEXT NOT NULL,
	"completed"	INTEGER NOT NULL DEFAULT 0 CHECK("completed" IN (0, 1)),
	"deadline"	TEXT,
	PRIMARY KEY("pwidget_id"),
	FOREIGN KEY("pwidget_id") REFERENCES "project_widgets"("pwidget_id") ON DELETE CASCADE,
	FOREIGN KEY("title") REFERENCES "project_widgets"("content")
);

""","""

CREATE TABLE "task_widgets" (
	"twidget_id"	INTEGER NOT NULL,
	"pwidget_id"	INTEGER NOT NULL,
	"widget_type"	TEXT NOT NULL CHECK("widget_type" IN ("Header", "Paragraph")),
	"content"	TEXT NOT NULL,
	"display_order"	INTEGER,
	PRIMARY KEY("twidget_id" AUTOINCREMENT),
	FOREIGN KEY("pwidget_id") REFERENCES "project_widgets"("pwidget_id") ON DELETE CASCADE
);""",
    """
CREATE TRIGGER auto_increment_pw_display_order
BEFORE INSERT ON project_widgets
FOR EACH ROW
WHEN NEW.display_order IS NULL
BEGIN
    UPDATE project_widgets
    SET display_order = (
        SELECT COALESCE(MAX(display_order), 0) + 1
        FROM project_widgets
        WHERE project_id = NEW.project_id
    )
    WHERE rowid = NEW.rowid;
END;

""",
"""
CREATE TRIGGER auto_increment_tw_display_order
BEFORE INSERT ON task_widgets
FOR EACH ROW
WHEN NEW.display_order IS NULL
BEGIN
    UPDATE task_widgets
    SET display_order = (
        SELECT COALESCE(MAX(display_order), 0) + 1
        FROM task_widgets
        WHERE pwidget_id = NEW.pwidget_id
    )
    WHERE rowid = NEW.rowid;
END;
""",


"""
CREATE TRIGGER insert_task_data_after_widget
AFTER INSERT ON project_widgets
FOR EACH ROW
WHEN NEW.widget_type = 'Task'
BEGIN
    INSERT INTO task_data (pwidget_id, title)
    VALUES (NEW.pwidget_id, NEW.content);
END;

"""
]
queries = ["INSERT INTO task_widgets (pwidget_id, widget_type, content, display_order) VALUES (?, ?, ?, (SELECT COALESCE(MAX(display_order), 0) + 1 FROM task_widgets WHERE pwidget_id = ?));"]

for i, query in enumerate(queries):
    try:
        cursor.execute(query, [3, "Paragraph", "Paragraph for task with pwidget id 3", 3])
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

def add_to_json(query, query_name):
    import json
    with open("sqlite_functions.json", "r") as f:
        data = json.load(f)
    data[query_name] = query
    with open("sqlite_functions.json", "w") as json_file:
        json.dump(data, json_file, indent=4)
