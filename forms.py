from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Optional
from wtforms.fields import DateTimeLocalField

class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

class RegisterForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Подтвердите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')

class PollForm(FlaskForm):
    title = StringField('Название опроса', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Описание', validators=[Optional(), Length(max=500)])
    deadline = DateTimeLocalField('Срок окончания (необязательно)', format='%Y-%m-%dT%H:%M', validators=[Optional()])
    creator_name = StringField('Ваше имя', validators=[Optional(), Length(max=100)])
    submit = SubmitField('Создать опрос')

class OptionForm(FlaskForm):
    name = StringField('Название опции', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Описание', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Добавить опцию')

class VoteForm(FlaskForm):
    voter_name = StringField('Ваше имя', validators=[DataRequired(), Length(max=100)])
    submit = SubmitField('Отправить голос')