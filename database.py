from flask_sqlalchemy import SQLAlchemy
from app import *

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'

db = SQLAlchemy(app)

class students(db.Model):
    id = db.Column('student_id', db.Integer, primary_key = True)
    username = db.Column(db.String(15))
    email = db.Column(db.String(50))
    
def __init__(self, username, email):
   self.username = username
   self.email = email

