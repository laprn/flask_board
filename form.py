from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email, Length
from wtforms.fields import HiddenField, EmailField, PasswordField, URLField, TextAreaField
from wtforms import StringField, ValidationError
from model import User

class LoginForm(FlaskForm):
    email = EmailField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired(), Length(8)])

class PostForm(FlaskForm):
    title = StringField('title', validators=[DataRequired(), Length(max=32)])
    url = URLField('url', validators=[DataRequired(), Length(max=64)])
    author_id = HiddenField('author_id', validators=[DataRequired()])

class UpdateForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(max=16)])
    about = TextAreaField('about', validators=[Length(max=64)])
