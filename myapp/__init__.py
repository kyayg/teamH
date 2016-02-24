import os
from flask import Flask, render_template, redirect
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager

from flask.ext.migrate import Migrate, MigrateCommand

from flask.ext.bootstrap import Bootstrap



app = Flask(__name__)
app.config.from_object('config')
manager = Manager(app)


app.config['SQLALCHEMY_DATABASE_URI'] =\
            'sqlite:///' + os.path.join(basedir, 'main.db')

db = SQLAlchemy(app)

migrate = Migrate(app,db)
manager.add_command('db', MigrateCommand)

Bootstrap(app)

import myapp.views

