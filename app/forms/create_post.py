from django.db.models import TextField
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length


class PostForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])

    text = TextField('Напишите что-нибудь...', validators=[Length(min=8)])

    category = SelectField('Категория', choices=[(1, 'music'),
                                                 (2, 'funny'),
                                                 (3, 'videos'),
                                                 (4, 'programming'),
                                                 (5, 'news'),
                                                 (6, 'fashion'),
                                                 (7, 'aviation'),])
    submit = SubmitField('Опубликовать')