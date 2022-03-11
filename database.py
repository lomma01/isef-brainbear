import sqlite3

conn = sqlite3.connect('database.db')
print ("Opened database successfully")
#columns -> you also have to change it in @app.route('/callback')!!!
conn.execute('CREATE TABLE students (id INTEGER NOT NULL PRIMARY KEY,nickname TEXT NOT NULL, user_id TEXT NOT NULL)')
print ("Table created successfully")
conn.close()
