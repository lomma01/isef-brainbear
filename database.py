import sqlite3 as sql
from sqlite3 import Error

class DatabaseManager(object):
    def __init__(self):
        self.conn = sql.connect('database.db')
        self.conn.execute('pragma foreign_keys = on')
        self.conn.commit()
        self.cur = self.conn.cursor()

    def query(self, query):
        self.cur.execute(query)
        self.conn.commit()
        return self.cur
    
    def fetch_all_user_rows(self):

        with self.conn:
            self.conn.row_factory = sql.Row
            curs = self.conn.cursor()
            curs.execute("SELECT * FROM users")
            rows = curs.fetchall()
            return rows


def database_query(query):
    connect_to_sql_db = sql.connect('database.db')
    connect_to_sql_db.cursor().execute(query)

def create_user_table():
    query_users_table = (''' CREATE TABLE IF NOT EXISTS users 
                      (id         TEXT    PRIMARY KEY,
                        username    TEXT    NOT NULL,
                       role        TEXT    NOT NULL
                      );''')

    DatabaseManager().query(query_users_table)

def create_modules_table():
    global query_modules_table
    query_modules_table = (''' CREATE TABLE IF NOT EXISTS modules 
                     (id             TEXT    PRIMARY KEY,
                     designation     TEXT    NOT NULL,
                     module     TEXT    NOT NULL
                     );''')

    DatabaseManager().query(query_modules_table)

def create_highscore_table():
    query_highscore_table = (''' CREATE TABLE IF NOT EXISTS highscores 
                            (id             TEXT    PRIMARY KEY,
                            user_id         TEXT    NOT NULL,
                            module     TEXT    NOT NULL,
                            highscore       INT,
                            FOREIGN KEY(user_id) REFERENCES users(id),
                            FOREIGN KEY(module) REFERENCES modules(id)
                            );''')

    DatabaseManager().query(query_highscore_table)

def create_all_tables():
    create_user_table()
    create_modules_table()
    create_highscore_table()
    
create_all_tables()