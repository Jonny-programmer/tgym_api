from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length, Email


class RegisterForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=4)])

    name = StringField('Введите имя', validators=[DataRequired()])
    surname = StringField('Введите фамилию', validators=[DataRequired()])
    email = StringField('Введите адрес почты', validators=[DataRequired(), Email()])

    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=8, max=20)])
    password_again = PasswordField('Введите пароль еще раз', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Создать аккаунт')