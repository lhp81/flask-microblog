from flask import Flask, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand
from flask import render_template
from flask.ext.bootstrap import Bootstrap


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flaskblog'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

bootstrap = Bootstrap(app)

manager = Manager(app)
manager.add_command('db', MigrateCommand)


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True)
    body = db.Column(db.Text)
    pub_date = db.Column(db.DateTime)
    author = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, title, body, author, pub_date=None):
        self.title = title
        self.body = body
        if pub_date is None:
            pub_date = datetime.utcnow()
        self.pub_date = pub_date
        self.author = author

    def __repr__(self):
        return '<Post %r>' % self.title


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    password = db.Column(db.String(40))
    email = db.Column(db.String)

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username


# def write_post(title=None, text=None, author):
#     new_post = Post(title, text, author)
#     db.session.add(new_post)
#     db.session.commit()


def read_posts():
    """Display posts in reverse order."""
    all_posts = Post.query().order_by(Post.id.desc()).all()
    # the above was taken from our in-class code review
    return all_posts


def read_post(id):
    the_post = Post.query.filter_by(id=id).first()
    if not Post:
        raise IndexError('Someone there is who cannot find a post.\n'
                         'Oh, it\'s you!\n'
                         'That post doesn\'t exist!')
    else:
        return the_post


def add_user(username=None, email=None, password=None):
    if username==None:
        messages.append('No anonymous artists allowed. Pick a name, pilgrim.')
    if email==None:
        messages.append('No, no, no. You have to enter a (valid) email.')
    if password==None:
        messages.append('No password=your shit gets jacked. The internet is '
                        'like Sparta with cat gifs. Enter a password, genius.')


@app.route('/')
def all_posts():
    # posts = read_posts()
    return render_template('base.html')


@app.route('/compose', methods=['GET', 'POST'])
def write_post():
    return render_template('compose.html')


@app.route('/usercontrol')
def login_register():
    return render_template('usercontrol.html')

if __name__ == '__main__':
    manager.run()
