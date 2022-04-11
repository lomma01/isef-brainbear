import sqlite3 as sql

DATABASE = 'database_db'


class DatabaseManager(object):
    def __init__(self):
        self.conn = sql.connect(DATABASE)
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


class UpdateTables:
    def __init__(self):
        self.conn = sql.connect(DATABASE)
        self.cur = self.conn.cursor()

    def update_module_name(self, new_name, module_name):
        query_update_module_name = """UPDATE OR IGNORE modules SET module_name = ? WHERE module_name = ?"""
        query_update_all_related_questions = """UPDATE OR IGNORE questions SET module_name = ? WHERE module_name = ?"""
        data = [new_name, module_name]
        self.cur.execute(query_update_module_name, data)
        self.cur.execute(query_update_all_related_questions, data)
        self.conn.commit()

    def update_question_columns(self, column_name_that_will_be_changed,
                                changed_value, name_of_question_to_be_changed):
        if column_name_that_will_be_changed == "module_name":
            query = """UPDATE questions SET module_name = ? WHERE question = ?"""
        if column_name_that_will_be_changed == "chapter":
            query = """UPDATE questions SET chapter = ? WHERE question = ?"""
        if column_name_that_will_be_changed == "question":
            query = """UPDATE questions SET question = ? WHERE question = ?"""
        if column_name_that_will_be_changed == "correct_answer":
            query = """UPDATE questions SET correct_answer = ? WHERE question = ?"""
        if column_name_that_will_be_changed == "wrong_answer_1":
            query = """UPDATE questions SET wrong_answer_1 = ? WHERE question = ?"""
        if column_name_that_will_be_changed == "wrong_answer_2":
            query = """UPDATE questions SET wrong_answer_2 = ? WHERE question = ?"""
        if column_name_that_will_be_changed == "wrong_answer_3":
            query = """UPDATE questions SET wrong_answer_3 = ? WHERE question = ?"""
        if column_name_that_will_be_changed == "hint":
            query = """UPDATE questions SET hint = ? WHERE question = ?"""

        data = [changed_value, name_of_question_to_be_changed]
        self.cur.execute(query, data)
        self.conn.commit()


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
                            highscore       INT
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
                            hint                TEXT
                            );''')

    DatabaseManager().query(query_question_table)


def create_all_tables():
    create_user_table()
    create_modules_table()
    create_highscore_table()
    create_question_table()


create_all_tables()
