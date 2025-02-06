import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('data.db')
cursor = conn.cursor()

# Step 1: Create a new table with AUTOINCREMENT on field_id and a composite primary key
cursor.execute("")

# Commit the changes and close the connection
conn.commit()
conn.close()
