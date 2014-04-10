# 99 chars across? yeah baby, I read two scoops of django.

import string
from random import choice
from flask import (Flask, session, url_for, render_template, redirect, flash,
                   request)
from flask.ext.seasurf import SeaSurf
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.bootstrap import Bootstrap
from flask_mail import Mail, Message
from passlib.apps import custom_app_context as pwd_context
from flaskext.bcrypt import Bcrypt


app = Flask(__name__)

bcrypt = Bcrypt(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flaskblog'
# app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# app.config['MAIL_PORT']= 465
# app.config['MAIL_USE_SSL'] = True
# app.config['MAIL_USERNAME'] = '@gmail.com'
# app.config['MAIL_PASSWORD'] = 'modernartisbullshitandi\'maphilistine'
# app.config['MAIL_DEFAULT_SENDER'] = ('the head poet', 'microflaskinpoetry@gmail.com')

app.secret_key = 'thiskeyissecret'

db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

bootstrap = Bootstrap(app)

csrf = SeaSurf(app)

mail = Mail(app)

# set up the database.

categories = db.Table('categories',
                      db.Column('category_id', db.Integer, db.ForeignKey('category.id')),
                      db.Column('post_id', db.Integer, db.ForeignKey('post.id'))
                      )


class Post(db.Model):
    # __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True)
    body = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    poet = db.Column(db.String(80))
    pub_date = db.Column(db.DateTime)
    category = db.relationship('Category', backref=db.backref('posts', lazy='dynamic'))

    def __init__(self, title, body, author, category, pub_date=None):
        self.title = title
        self.body = body
        self.author = author
        self.category = category
        if pub_date is None:
            pub_date = datetime.utcnow()
        self.pub_date = pub_date

    def __repr__(self):
        return '<Post %r>' % self.title


class User(db.Model):
    # __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(128))
    email = db.Column(db.String, unique=True)
    confirmation_key = db.Column(db.String(20))
    confirmed = db.Column(db.Boolean, default=False)
    user_posts = db.relationship("Post", backref="author", lazy='dynamic')

    def __init__(self, username, password, email):
        self.username = username
        self.password = bcrypt.generate_password_hash(password)
        self.email = email
        self.confirmation_key = create_registration_key()
        self.confirmed = False

    def __repr__(self):
        return '<User %r>' % self.username


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    def __init__(self, category_name):
        self.category_name = category_name

    def __repr__(self):
        return '<Category %r>' % self.category_name

# here are the helper functions.


def write_post(title, text, poet, author):
    user = User.query.filter_by(username=request.form['username']).first()
    if user.confirmed is False:
        flash('You need to confirm your account before you can post.')
        render_template('compose.html')
    if title and text and poet:
        new_post = Post(title, text, author, poet)
        db.session.add(new_post)
        db.session.commit()
        flash('Thanks for your contribution.')
    else:
        flash("A poem isn't a poem without a title, a poet, and some content.\n"
              "Don't get all cute and post-modern on me. Fill that shit out.")


def read_posts():
    """Display posts in reverse order."""
    return Post.query.order_by(Post.id.desc()).all()


def read_poem(id):
    """Retrieve a single post by its id."""
    post = Post.query.get(id)
    if post is None:
        flash('Sorry, that post doesn\'t exist.')
        return redirect(url_for('all_posts'))
    return post


def create_registration_key():
    return ''.join(choice(string.letters) for i in range(20))


def add_user(username, email, password):
    if username is None:
        flash('No anonymous poets allowed. Pick a name, pilgrim.')
        return redirect(url_for('register'))
    elif email is None:
        flash('No, no, no. You have to enter a (valid) email.')
        return redirect(url_for('register'))
    elif password is None:
        flash('Enter a password, amigo. This isn\'t a perfect world.')
        return redirect(url_for('register'))
    else:
        pass

# and now for our views.


@app.route('/')
def all_posts():
    the_posts = read_posts()
    return render_template('base.html', posts=the_posts)


@app.route('/compose', methods=['GET', 'POST'])
def add_poem():
    if 'logged_in' in session and session['logged_in']:
        if request.method == "POST":
            write_post(request.form['title'],
                       request.form['body'],
                       request.form['poet'],
                       session['current_user'])
            return redirect(url_for('all_posts'))
    return render_template('compose.html')


@app.route('/usercontrol', methods=['GET', 'POST'])
def login_register():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user:
            if bcrypt.generate_password_hash(request.form['password']) == user.password:
                session['logged_in'] = True
                session['current_user'] = request.form['username']
                flash("You are logged in. Whoopty-doo.")
                return redirect(url_for('all_posts'))
        else:
            flash('Dude[ette], you muffed it. Try logging in again.')
    return render_template('usercontrol.html')


@app.route('/register', methods=['GET', 'POST'])
def register_user():
    # if request.method == 'POST':
    #     asdf
    #     if x:
    #         y
    #     else:
    #         flash('Thanks for registering. Check your email for a confirmation link.')
    #         return render_template('base.html')
    return render_template('register.html')


@app.route('/confirm/<string:conf_key>')
def confirm_user():
    pass


@app.route('/categories')
def show_categories():
    return render_template('categories.html')


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    session.pop('logged_in', None)
    session.pop('user_id', None)
    flash('You were logged out -- see you next time!')
    return redirect(url_for('all_posts'))


@app.route('/<id>')
def single_poem(id):
    poem = read_poem(id)
    return render_template('poem.html', post=poem)


if __name__ == '__main__':
    manager.run()
