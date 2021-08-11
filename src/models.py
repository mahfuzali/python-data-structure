import sys
import pathlib

base_path = pathlib.Path(__file__).resolve().parents[2]
sys.path.append(str(base_path))

from sqlite3 import Connection as SQLite3Connection
from datetime import datetime
from sqlite3.dbapi2 import Binary
from sqlalchemy import event
from sqlalchemy.engine import Engine
from flask import Flask, json, request, jsonify
from sqlalchemy import event
from sqlalchemy.engine import Engine
from flask_sqlalchemy import SQLAlchemy

# app
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sqlitedb.file"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = 0

db = SQLAlchemy(app)
now = datetime.now()

# models
# configure sqlite3 to enforce foreign key contraints
@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()


# models
class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    address = db.Column(db.String(200))
    phone = db.Column(db.String(50))
    posts = db.relationship("BlogPost", cascade="all, delete")

    def __eq__(self, other):
        return ((self.email, self.name) == (other.email, other.name))

    def __ne__(self, other):
        return ((self.email, self.name) != (other.email, other.name))

    def __lt__(self, other):
        return ((self.email, self.name) < (other.email, other.name))

    def __le__(self, other):
        return ((self.email, self.name) <= (other.email, other.name))

    def __gt__(self, other):
        return ((self.email, self.name) > (other.email, other.name))

    def __ge__(self, other):
        return ((self.email, self.name) >= (other.email, other.name))

    # def __repr__(self):
    #     return "%s %s" % (self.name, self.email)

class BlogPost(db.Model):
    __tablename__ = "blog_post"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    body = db.Column(db.String(200))
    date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
