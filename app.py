from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin, LoginManager, login_user, login_required, current_user, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length
from wtforms.widgets import TextArea
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'thesecretkey'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

with app.app_context():
    db = SQLAlchemy(app)
    bcrypt = Bcrypt(app)

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

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(30), nullable=False)
    role = db.Column(db.String(10), nullable=False)
    posts = db.relationship('Post', backref='author')

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

class LoginForm(FlaskForm):
    username = StringField(validators=[
        InputRequired(), Length(min=6, max=20)
    ], render_kw={
        'placeholder': 'username...'
    })
    password = PasswordField(validators=[
        InputRequired(), Length(min=6, max=20)
    ], render_kw={
        'placeholder': 'password...'
    })
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField(validators=[
        InputRequired(), Length(min=6, max=20)
    ], render_kw={
        'placeholder': 'username...'
    })
    password = PasswordField(validators=[
        InputRequired(), Length(min=6, max=20)
    ], render_kw={
        'placeholder': 'password...'
    })
    submit = SubmitField('Register')

class PostForm(FlaskForm):
    title = StringField(validators=[InputRequired()])
    content = StringField(validators=[InputRequired()], widget=TextArea())
    tags = StringField(validators=[InputRequired()])
    submit = SubmitField('Create Post')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('dashboard'))

    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(name=form.username.data, username=form.username.data, password=hashed_password, role='Author')
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', user=current_user)

@app.route('/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    content=form.content.data)
        post.author = current_user
        form.title.data = ''
        form.content.data = ''
        form.tags.data = ''
        db.session.add(post)
        db.session.commit()
        return render_template('new.html', form=form)
    else:
        return render_template('new.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
