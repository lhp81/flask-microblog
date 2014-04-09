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


class Post(db.Model):
    # __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True)
    body = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    poet = db.Column(db.String(80))
    pub_date = db.Column(db.DateTime)

    def __init__(self, title, body, author, pub_date=None):
        self.title = title
        self.body = body
        self.author = author
        # self.category = category
        if pub_date is None:
            pub_date = datetime.utcnow()
        self.pub_date = pub_date

    def __repr__(self):
        return '<Post %r>' % self.title


# class Category(db.Model):
#     __tablename__ = 'categories'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50))

#     def __init__(self, name):
#         self.name = name

#     def __repr__(self):
#         return '<Category %r>' % self.name


class User(db.Model):
    # __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String, unique=True)
    user_posts = db.relationship("Post", backref="author", lazy='dynamic')
    # confirmed = db.Column(db.Boolean)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
        # self.confirmed = False

    def __repr__(self):
        return '<User %r>' % self.username


def write_post(title, text, poet, author):
    if title and text:
        new_post = Post(title, text, author)
        db.session.add(new_post)
        db.session.commit()
    else:
        flash("A poem isn't a poem without a title and some content.\n"
              "Don't get all cute and post-modern on me.")


def read_posts():
    """Display posts in reverse order."""
    return Post.query.order_by(Post.id.desc()).all()


def add_user(username, email, password):
    if username==None:
        flash('No anonymous poets allowed. Pick a name, pilgrim.')
    elif email==None:
        flash('No, no, no. You have to enter a (valid) email.')
    elif password==None:
        flash('Enter a password, amigo. This isn\'t a perfect world.')
    else:
        if username and email and password:
            pass



@app.route('/')
def all_posts():
    the_posts = read_posts()
    return render_template('base.html', posts=the_posts)


@app.route('/compose', methods=['GET', 'POST'])
def add_poem():
    if 'logged_in'in session and session['logged_in']:
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
        if user and request.form['password'] == user.password:
            session['logged_in'] = True
            session['current_user'] = request.form['username']
            flash("You are logged in. Whoopty-doo.")
            return redirect(url_for('all_posts'))
        else:
            flash('Dude, you muffed it. Try logging in again.')
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
    return render_template('poem.html', post=poem, orig_poet=poet)

def read_poem(id):
    """Retrieve a single post by its id."""
    post = Post.query.get(id)
    if post is None:
        flash('Sorry, that post doesn\'t exist.')
        return redirect(url_for('all_posts'))
    return post

if __name__ == '__main__':
    manager.run()
