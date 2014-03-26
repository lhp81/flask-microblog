from flask import (Flask, session, url_for, render_template, redirect, flash,
                   request)
from flask.ext.seasurf import SeaSurf
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from flask.ext.bootstrap import Bootstrap


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flaskblog'
app.secret_key = 'thiskeyissecret'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
bootstrap = Bootstrap(app)
csrf = SeaSurf(app)


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True)
    body = db.Column(db.Text)
    author = db.Column(db.String)
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
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(40))
    email = db.Column(db.String, unique=True)
    # confirmed = db.Column(db.Boolean)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
        # self.confirmed = False

    def __repr__(self):
        return '<User %r>' % self.username


def write_post(title, text, author):
    if title and text:
        new_post = Post(title, text, author)
        db.session.add(new_post)
        db.session.commit()
    else:
        flash("A post isn't a post without a title and some content.")


def read_posts():
    """Display posts in reverse order."""
    return Post.query().order_by(Post.id.desc()).all()

# def read_post(id):
#     the_post = Post.query.filter_by(id=id).first()
#     if not Post:
#         raise IndexError('Someone there is who cannot find a post.\n'
#                          'Oh, it\'s you!\n'
#                          'That post doesn\'t exist!')
#     else:
#         return the_post


def add_user(username=None, email=None, password=None):
    if username==None:
        flash('No anonymous poets allowed. Pick a name, pilgrim.')
    elif email==None:
        flash('No, no, no. You have to enter a (valid) email.')
    elif password==None:
        flash('Enter a password, amigo. This isn\'t a perfect world.')


@app.route('/')
def all_posts():
    posts = read_posts()
    return render_template('base.html', posts=posts)


@app.route('/compose', methods=['GET', 'POST'])
def add_poem():
    if 'logged_in'in session and session['logged_in']:
        if request.method == "POST":
            try:
                # author = User.username == session['current_user']
                write_post(request.form['title'],
                           request.form['body'],
                           session['current_user'])
                return redirect(url_for('all_posts'))
            except ValueError:
                flash("Error: title and text required")
    return render_template('compose.html')


@app.route('/usercontrol', methods=['GET', 'POST'])
def login_register():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and request.form['password'] == user.password:
            session['logged_in'] = True
            session['current_user'] = request.form['username']
            flash('You are logged in')
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

# @app.route('/post/<id>', method='GET')
# def single_post_view():
#     return render_template('single_post.html', id=id)

if __name__ == '__main__':
    manager.run()
