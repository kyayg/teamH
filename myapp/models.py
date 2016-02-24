from myapp import app, db

from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import LoginManager, UserMixin, login_required

from flask.ext.login import LoginManager, login_required, UserMixin

login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin, db.Model):
    """
    とりあえず、ユーザーの名前とメアドとパスワード（ハッシュ後）
    回生、学部、等々は略
    """
    __tablename__ = 'user'

    uid = db.Column(db.Integer, primary_key=True)  # USER ID, PRIMARY

    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)

    year = db.Column(db.Integer)

    user_id = db.relationship('Article', backref='user')

    password_hash = db.Column(db.String(128))


    def __init__(self):
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

    aid = db.Column(db.Integer, primary_key=True)  # ARTICLE ID, PRIMARY

    author_id = db.Column(db.Integer, db.ForeignKey('user.uid'))
    title = db.Column(db.String(512))
    body = db.Column(db.Text)
    published_on = db.Column(db.DateTime)

    def __init__(self):
        self.author_id = None
        self.title = None
        self.body = None


def hello():
    return "Hello"


if __name__ == "__main__":
    db.create_all()
