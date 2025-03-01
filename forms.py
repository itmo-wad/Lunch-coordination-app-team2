from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional
from wtforms.fields import DateTimeLocalField

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=64)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class PollForm(FlaskForm):
    title = StringField('Poll Title', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[Optional(), Length(max=500)])
    deadline = DateTimeLocalField('Deadline (optional)', format='%Y-%m-%dT%H:%M', validators=[Optional()])
    creator_name = StringField('Your Name', validators=[Optional(), Length(max=100)])
    submit = SubmitField('Create Poll')

class OptionForm(FlaskForm):
    name = StringField('Option Name', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Add Option')

class VoteForm(FlaskForm):
    voter_name = StringField('Your Name', validators=[DataRequired(), Length(max=100)])
    submit = SubmitField('Submit Vote')