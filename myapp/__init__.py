from flask import Flask, render_template, redirect
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager

import os


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
manager = Manager(app)


app.config['SQLALCHEMY_DATABASE_URI'] =\
            'sqlite:///' + os.path.join(basedir, 'db')

db = SQLAlchemy(app)

@app.route('/')
def index():

    return 'HelloWorld'


@app.route('/register')
def register():

    return "This is register page"

@app.route('/login')
def login():

    return "This is login page"

@app.route('/logout')
def logout():

    return "click logout button, redirect / "








