from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class DishForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    is_private = BooleanField("Сохранить блюдо в профиль")
    submit = SubmitField('Применить')