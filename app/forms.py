from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, StringField, PasswordField, DateTimeField
from wtforms.validators import DataRequired, InputRequired, EqualTo, Optional, Length
from .models import User
from wtforms.fields.html5 import DateTimeLocalField
from datetime import datetime, timedelta


class LoginForm(FlaskForm):
    username = StringField('Введите имя пользователя', validators=[InputRequired(message='Поле не должно быть пустым'), Length(max=64)])
    password = PasswordField('Введите пароль', validators=[InputRequired(message='Поле не должно быть пустым')])
    password2 = PasswordField('Повторите пароль', validators=[EqualTo('password', message='Пароли не совпадают'), Optional(),])
    submit = SubmitField('OK')


class EventForm(FlaskForm):
    time_begin = DateTimeLocalField('Дата начала', format='%Y-%m-%dT%H:%M')
    time_end = DateTimeLocalField('Дата конца', format='%Y-%m-%dT%H:%M')
    subject = StringField('Тема', validators=[DataRequired(message='Поле не должно быть пустым'), Length(max=128)])
    description = TextAreaField('Описание события')
    submit = SubmitField('OK')
