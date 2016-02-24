from flask import render_template
from myapp import app






@app.route('/')
@app.route('/<name>')
def index(name=None):

    return render_template('index.html',name = name)


@app.route('/register')
def register():
    username = None
    form = None


    return render_template('register.html')

@app.route('/login')
def login():

    return "This is login page"

@app.route('/logout')
def logout():

    return "click logout button, redirect / "



