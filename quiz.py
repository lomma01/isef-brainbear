import sqlite3 as sql

def dict_factory(cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

con = sql.connect('database.db')
cur = con.cursor()
con.row_factory = dict_factory
cur.execute("select * from questions")
tupel = cur.fetchall()
quiz_id = tupel[0]
