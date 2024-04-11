import datetime
import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Dishes(SqlAlchemyBase):
    __tablename__ = 'dishes'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    calories = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    size = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    protein = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    sodium = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    potassium = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    cholesterol = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    carbohydrates_total = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    fiber = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    sugar = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    is_private = sqlalchemy.Column(sqlalchemy.Boolean, default=True)

    user_id = sqlalchemy.Column(sqlalchemy.Integer,
                                sqlalchemy.ForeignKey("users.id"))
    user = orm.relationship('User')