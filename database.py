import sqlite3

conn = sqlite3.connect('database.db')
print ("Opened database successfully")

conn.execute('CREATE TABLE students (id INTEGER NOT NULL PRIMARY KEY,name TEXT NOT NULL, nickname TEXT NOT NULL, user_id TEXT NOT NULL)')
print ("Table created successfully")
conn.close()
