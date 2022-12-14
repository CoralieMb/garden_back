from flask import current_app, g
from flask_sqlalchemy import SQLAlchemy

#Create an instance of MySQL

def get_db():
    if 'db' not in g:
        g.db = SQLAlchemy(current_app)
    return g.db

def close_db(e=None):
    db = g.pop('db', None)

 