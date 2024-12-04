import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('cricket_data.db')
cursor = conn.cursor()

# Select and print all records from the cricket_matches table
cursor.execute('SELECT * FROM cricket_matches')
rows = cursor.fetchall()

for row in rows:
    print(row)

# Close connection
conn.close()


