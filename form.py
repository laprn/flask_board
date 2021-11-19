from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email, Length
from wtforms.fields import HiddenField, EmailField, PasswordField, TextAreaField
from wtforms import StringField, ValidationError

class LoginForm(FlaskForm):
    email = EmailField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[DataRequired(), Length(8)])

class PostForm(FlaskForm):
    title = StringField('title', validators=[DataRequired(), Length(max=32)])
    content = TextAreaField('content', validators=[DataRequired(), Length(max=64)])
    author_id = HiddenField('author_id', validators=[DataRequired()])