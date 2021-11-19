from flask import Flask, render_template, redirect, flash
from flask_login.utils import login_required, logout_user
from flask_sqlalchemy import SQLAlchemy
from flask.globals import request
from flask.helpers import url_for
from flask_login import LoginManager, login_user, current_user
from model import User, Post
from form import LoginForm, PostForm, UpdateForm
import hashlib

app = Flask(__name__)
app.secret_key = 'fefpaojpoaiefjpoiajo'  # Change this!

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.user'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "users.login"

def is_valid(user_mail, user_password):
    flag = 0
    user = User.query.filter_by(email=user_mail).first()
    if user:
        flag = user.password == hashlib.md5(user_password.encode()).hexdigest()
    return flag


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/')
def index():
    users_post = db.session.query(Post, User).join(Post, User.id == Post.author_id).all()
    return render_template('index.html', posts=users_post)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'GET':
        return render_template('login.html', form=form)
    else:
        if form.validate_on_submit():
            user_mail = form.email.data
            user_password = form.password.data      
            if is_valid(user_mail, user_password):
                user = User.query.filter_by(email=user_mail).first()
                login_user(user)
                flash('Logged in.')
                next = request.args.get('next')
                return redirect(next or url_for('index'))
            else:
                flash('Login failed.')
                return redirect(url_for('login'))

@app.route('/signup', methods=['POST'])
def signup():
    form = LoginForm()
    if form.validate_on_submit():
        user_mail = form.email.data
        user_password = form.password.data
    
    hash = hashlib.md5(user_password.encode()).hexdigest()
    reg_user = User(email=user_mail, password=hash)
    db.session.add(reg_user)
    db.session.commit()

    flash('Sign up completed.')
    return redirect('login')

@app.route('/post', methods=['GET', 'POST'])
@login_required
def post():
    form = PostForm()
    if request.method == 'GET':
        return render_template('post.html', form=form)
    else:
        title = form.title.data
        url = form.url.data

        post = Post(title=title, url=url, author_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('index'))


@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateForm()
    if request.method == 'GET':
        form.username.data = current_user.username
        form.about.data = current_user.about
        return render_template('account.html', form=form)
    else:
        db.create_all()
        id = current_user.id
        username = form.username.data
        about = form.about.data
        username_exist = User.query.filter_by(username=username).first()
        if username_exist:
            flash('this username has already exist. try another one.')
            return redirect(url_for('account'))
        user = User.query.get(id)
        user.username = username
        user.about = about
        db.session.merge(user)
        db.session.commit()
        flash('update complited.')
        return render_template('account.html', form=form)

@app.route('/user/<string:username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    return render_template('user.html', user=user)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
