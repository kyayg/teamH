from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

from flask.ext.login import UserMixin

import os


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'user.sqlite')

app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)


class User(UserMixin, db.Model):
    """
    とりあえず、ユーザーの名前とメアドとパスワード（ハッシュ後）
    回生、学部、等々は略
    """
    __tablename__ = 'userdb'

    uid = db.Column(db.Integer, primary_key = True)# USER ID, PRIMARY

    username = db.Column(db.String(64), unique = True, index = True)
    email = db.Column(db.String(64), unique = True, index = True)
    userid = db.relationship('Article', backref='role')

    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        """
        パスワード　ハッシュ化
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        ハッシュ化（パスワード（生）） == バスワード（ハッシュ）
        -> True
        """
        return check_password_hash(self.password_hash, password)


class Article(db.Model):
    """
    本文記事　まわり
    """
    __tablename__ = 'articledb'

    aid = db.Column(db.Integer, primary_key = True) # ARTICLE ID, PRIMARY

    author_id = db.Column(db.Integer, db.ForeignKey('user.uid'))
    title = db.Column(db.String(512) )
    body = db.Column(db.Text)



@app.route('/signin')
def signin():
    render_template("./templates/signin.html")


@app.route('/login')
def login():
    render_template("./templates/login")



@app.route('/index')
@app.login_required
def testes():
    render_template("./test.html")




if __name__ == "__main__":

    app.run()
