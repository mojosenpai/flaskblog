from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

with app.app_context():
    db = SQLAlchemy(app)

post_tag = db.Table('post_tag',
                    db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
                    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
                    )

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    image = db.Column(db.String(200))
    video = db.Column(db.String(200))
    content = db.Column(db.String(1000), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now())
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    labels = db.relationship('Tag', secondary='post_tag', backref='posts_labeled')

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(30), nullable=False)
    role = db.Column(db.String(10), nullable=False)
    posts = db.relationship('Post', backref='author')

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

@app.route('/')
def home():
    return 'Hello world!'

@app.route('/info')
def info():
    return 'This is a website written in Flask'

if __name__ == '__main__':
    app.run(debug=True)
