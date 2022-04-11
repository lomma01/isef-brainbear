import sqlite3 as sql

DATABASE = 'database.db'


class DatabaseManager(object):
    def __init__(self):
        self.conn = sql.connect(DATABASE)
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

    def fetch_all_module_rows(self):

        with self.conn:
            self.conn.row_factory = sql.Row
            curs = self.conn.cursor()
            curs.execute("SELECT * FROM modules")
            rows = curs.fetchall()
            return rows


def insert_user_into_user_table(user_id, username, role):
    try:
        connect_to_sql_db = sql.connect(DATABASE)

        query = """INSERT OR IGNORE INTO users (id,username,role) VALUES (?,?,?)"""
        data = (user_id, username, role)
        connect_to_sql_db.cursor().execute(query, data)
        connect_to_sql_db.commit()
        connect_to_sql_db.close()

    except sql.Error as error:
        print("Failed to insert user in user table", error)
    finally:
        if connect_to_sql_db:
            connect_to_sql_db.close()


def update_user_role(role, user_id):
    try:
        connect_to_sql_db = sql.connect(DATABASE)

        query = """UPDATE users SET role = ? WHERE id = ?"""
        data = (role, user_id)
        connect_to_sql_db.cursor().execute(query, data)
        connect_to_sql_db.commit()
        connect_to_sql_db.close()

    except sql.Error as error:
        print("Failed to update user table", error)
    finally:
        if connect_to_sql_db:
            connect_to_sql_db.close()


def database_query(query):
    connect_to_sql_db = sql.connect(DATABASE)
    connect_to_sql_db.cursor().execute(query)


def insert_question(module_name, chapter, question, correct_answer,
                    wrong_answer_1, wrong_answer_2, wrong_answer_3, hint):
    try:
        connect_to_sql_db = sql.connect(DATABASE)

        query = """INSERT INTO questions 
                (module_name,
                chapter,
                question,
                correct_answer,
                wrong_answer_1,
                wrong_answer_2,
                wrong_answer_3,
                hint)
                VALUES (?,?,?,?,?,?,?,?)"""
        data = [
            module_name, chapter, question, correct_answer, wrong_answer_1,
            wrong_answer_2, wrong_answer_3, hint
        ]
        connect_to_sql_db.cursor().execute(query, data)
        connect_to_sql_db.commit()
        connect_to_sql_db.close()

    except sql.Error as error:
        print("Failed to insert question", error)
    finally:
        if connect_to_sql_db:
            connect_to_sql_db.close()


def insert_module(module_name):
    try:
        connect_to_sql_db = sql.connect(DATABASE)

        query = """INSERT INTO modules 
                (module_name)
                VALUES (?)"""
        data = [module_name]
        connect_to_sql_db.cursor().execute(query, data)
        connect_to_sql_db.commit()
        connect_to_sql_db.close()

    except sql.Error as error:
        print("Failed to insert module", error)
    finally:
        if connect_to_sql_db:
            connect_to_sql_db.close()


#################
##table section##
#################
def create_user_table():
    query_users_table = (''' CREATE TABLE IF NOT EXISTS users 
                        (id         TEXT    PRIMARY KEY,
                        username    TEXT    NOT NULL,
                        role        TEXT    NOT NULL
                        );''')

    DatabaseManager().query(query_users_table)


def create_modules_table():
    query_modules_table = (''' CREATE TABLE IF NOT EXISTS modules 
                     (id            INTEGER    PRIMARY KEY AUTOINCREMENT,
                     module_name    TEXT    UNIQUE
                     );''')

    DatabaseManager().query(query_modules_table)


def create_highscore_table():
    query_highscore_table = (''' CREATE TABLE IF NOT EXISTS highscores 
                            (id             INTEGER    PRIMARY KEY AUTOINCREMENT,
                            user_id         TEXT    NOT NULL,
                            module_name     TEXT    NOT NULL,
                            highscore       INT,
                            FOREIGN KEY(user_id) REFERENCES users(id),
                            FOREIGN KEY(module_name) REFERENCES modules(id)
                            );''')

    DatabaseManager().query(query_highscore_table)


def create_question_table():
    query_question_table = (''' CREATE TABLE IF NOT EXISTS questions 
                            (id                 INTEGER    PRIMARY KEY AUTOINCREMENT,
                            module_name         TEXT    NOT NULL,
                            chapter             TEXT    NOT NULL,
                            question            TEXT    NOT NULL,
                            correct_answer      TEXT    NOT NULL,
                            wrong_answer_1      TEXT    NOT NULL,
                            wrong_answer_2      TEXT    NOT NULL,
                            wrong_answer_3      TEXT    NOT NULL,
                            hint                TEXT,
                            FOREIGN KEY(module_name) REFERENCES modules(id)
                            );''')

    DatabaseManager().query(query_question_table)


def create_all_tables():
    create_user_table()
    create_modules_table()
    create_highscore_table()
    create_question_table()


create_all_tables()
