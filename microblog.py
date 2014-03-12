from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from datetime import datetime
from flask.ext.script import Manager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =  \
    'postgresql://luke@localhost/flask-blog'
db = SQLAlchemy(app)
manager = Manager(app)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    body = db.Column(db.Text)
    pub_date = db.Column(db.DateTime)

    def __init__(self, title, body, pub_date=None):
        self.title = title
        self.body = body
        if pub_date is None:
            pub_date = datetime.utcnow()
        self.pub_date = pub_date

    def __repr__(self):
        return '<Post %r>' % self.title


def write_post(title, text):
    new_post = Post(title, text)
    db.session.add(new_post)
    db.session.commit()


def read_posts():
    """Display posts in reverse order."""
    pass


def read_post(id):
    the_post = Post.query.filter_by(id=id).first()
    if not Post:
        raise IndexError('That post doesn\'t exist!')
    else:
        return the_post

if __name__ == '__main__':
    pass
