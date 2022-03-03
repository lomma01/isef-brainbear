import sqlite3

conn = sqlite3.connect('database.db')
print ("Opened database successfully")

conn.execute('CREATE TABLE students (id INTEGER NOT NULL PRIMARY KEY,username TEXT NOT NULL, email TEXT NOT NULL)')
print ("Table created successfully")
conn.close()
