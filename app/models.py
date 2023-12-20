from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length
from flask_login import UserMixin
from sqlalchemy.sql import func
from app import db


class Article(db.Model):
    article_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(100), nullable=False)
    text = db.Column(db.String(80), unique=True, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f'<Article {self.intro}>'


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


# class ChangePasswordForm(FlaskForm):
#     old_password = PasswordField('Old Password', validators=[DataRequired()])
#     new_password = PasswordField('New Password', validators=[DataRequired()])
#     submit = SubmitField('Change Password')


# class Client(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(50), nullable=False)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


# class ClientForm(FlaskForm):
#     name = StringField('Client Name', validators=[DataRequired(), Length(min=2, max=50)])
#     submit = SubmitField('Add Client')


### add Note / start ###



### add Note / end ###
