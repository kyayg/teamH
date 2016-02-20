from flask import Flask, render_template, redirect
from flask.ext.sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.script import Manager

#from flask.ext.migrate import Migrate, MigrateCommand

from flask.ext.login import LoginManager, UserMixin, login_required

from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Required, Length, Email, Regexp, EqualTo
from wtforms import ValidationError

import os


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
manager = Manager(app)
app.config['SQLALCHEMY_DATABASE_URI'] =\
        'sqlite:///' + os.path.join(basedir, 'user.db')

app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True

db = SQLAlchemy(app)

#migrate = Migrate(app, db)
#manager.add_command('db', MigrateCommand)

login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin, db.Model):
    """
    とりあえず、ユーザーの名前とメアドとパスワード（ハッシュ後）
    回生、学部、等々は略
    """
    __tablename__ = 'user'

    uid = db.Column(db.Integer, primary_key = True)# USER ID, PRIMARY

    username = db.Column(db.String(64), unique = True, index = True)
    email = db.Column(db.String(64), unique = True, index = True)
    userid = db.relationship('Article', backref='user')

    password_hash = db.Column(db.String(128))


   def __init__():
       self.username = None
       self.email = None
       self.userid = None
       self.password_hash = None


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

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False


@login_manager.user_loader
def load_user(user_id):
        return User.get(user_id)


class Article(db.Model):
    """
    本文記事　まわり
    """
    __tablename__ = 'article'

    aid = db.Column(db.Integer, primary_key = True) # ARTICLE ID, PRIMARY

    author_id = db.Column(db.Integer, db.ForeignKey('user.uid'))
    title = db.Column(db.String(512) )
    body = db.Column(db.Text)
    published_on = db.Column(db.DateTime)
    def __init__():
        self.author_id = None
        self.title = None
        self.body = None



class RegistrationForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                           Email()])
    username = StringField('Username', validators=[
        Required(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                          'Usernames must have only letters, '
                                          'numbers, dots or underscores')])
    password = PasswordField('Password', validators=[
        Required(), EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[Required()])
    submit = SubmitField('Register')

#    def validate_email(self, field):
#        if User.query.filter_by(email=field.data).first():
#            raise ValidationError('Email already registered.')
#
#    def validate_username(self, field):
#        if User.query.filter_by(username=field.data).first():
#            raise ValidationError('Username already in use.')




@app.route('/signin')
def signin():
    render_template("./templates/signin.html")


@app.route('/login')
def login():
    render_template("./templates/login")



@app.route('/index')
def testes():
    render_template("./test.html")


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
#        send_email(user.email, 'Confirm Your Account',
#                   'auth/email/confirm', user=user, token=token)
#        flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('testes'))
    return render_template('./templates/login.html', form=form)



if __name__ == "__main__":
    db.create_all()
    manager.run()
