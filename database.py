import sqlite3

conn = sqlite3.connect('database.db')
#columns -> you also have to change it in @app.route('/callback')!!!

#you need foreign_keys = ON when you work with foreign keys in sqlite
#especially when you insert values into the tables with foreign keys
conn.execute("PRAGMA foreign_keys = ON")

#role = is_admin, is_dozent, is_student
query_users_table = (''' CREATE TABLE IF NOT EXISTS users 
                    (id         TEXT    PRIMARY KEY,
                    username    TEXT    NOT NULL,
                    role        TEXT    NOT NULL,
                    );''')

conn.execute(query_users_table)

query_modules_table = (''' CREATE TABLE IF NOT EXISTS modules 
                    (id             TEXT    PRIMARY KEY,
                    module_name     TEXT    NOT NULL
                    );''')

conn.execute(query_modules_table)

query_highscore_table = (''' CREATE TABLE IF NOT EXISTS highscores 
                    (id             TEXT    PRIMARY KEY,
                    user_id         TEXT    NOT NULL,
                    module_name     TEXT    NOT NULL,
                    highscore       INT,
                    FOREIGN KEY(user_id) REFERENCES users(id),
                    FOREIGN KEY(module_name) REFERENCES modules(id)
                    );''')

conn.execute(query_highscore_table)

conn.close()
