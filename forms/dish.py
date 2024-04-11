from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class SearchDishForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    mass = StringField('Вес, г', default=100)
    is_private = BooleanField("Не публиковать блюдо")
    submit = SubmitField('Найти')
    to_publish = SubmitField('Опубликовать и сохранить в профиль')