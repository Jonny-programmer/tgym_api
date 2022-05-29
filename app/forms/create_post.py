from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length


class CreatePostForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])

    content = TextAreaField('Напишите что-нибудь...', validators=[Length(min=8)])
    is_private = BooleanField('Сделать новость доступной только мне')
    category = SelectField('Категория', choices=['music', 'funny', 'videos', 'school'
                                                 'programming', 'news', 'fashion', 'aviation',
                                                 '---'])
    submit = SubmitField('Опубликовать')