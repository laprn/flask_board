from urllib.parse import urlsplit
from flask import Flask, render_template, redirect, flash
from flask_login.utils import login_required, logout_user
from flask_sqlalchemy import SQLAlchemy
from flask.globals import request
from flask.helpers import url_for
from flask_login import LoginManager, login_user, current_user
from model import User, Post
from form import LoginForm, PostForm
app = Flask(__name__)
app.secret_key = 'fefpaojpoaiefjpoiajo'  # Change this!

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.user'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "users.login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/')
def index():
    all_posts = Post.query.all()
    return render_template('index.html', posts=all_posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'GET':
        return render_template('login_get.html', form=form)
    else:
        if form.validate_on_submit():
            user_mail = form.email.data
            user_password = form.password.data

            print(f'user_mail:{user_mail},user_password:{user_password}')
            
            if User.query.filter_by(email=user_mail).first():
                user = User.query.filter_by(email = user_mail).first()
                if user.password == user_password:
                    login_user(user)
                    flash('Logged in.')
                    next = request.args.get('next')
                    return redirect(next or url_for('index'))
                else:
                    flash('Incorrect password.')
                    return redirect(url_for('login'))
            else:
                flash('Failed to login.')
                return redirect(url_for('login'))

@app.route('/post', methods=['GET', 'POST'])
@login_required
def post():
    form = PostForm()
    if request.method == 'GET':
        return render_template('post.html', form=form)
    else:
        title = form.title.data
        content = form.content.data

        post = Post(title=title, content=content, author_id=current_user.id)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('index'))

@app.route('/account')
@login_required
def account():
    return render_template('account.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
