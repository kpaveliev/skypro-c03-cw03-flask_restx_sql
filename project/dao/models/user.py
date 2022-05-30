from marshmallow import Schema, fields

from project.dao.models.base import BaseMixin
from project.setup_db import db


class User(BaseMixin, db.Model):
    __bind_key__ = 'users'
    __tablename__ = 'user'

    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    name = db.Column(db.String)
    surname = db.Column(db.String)
    favorite_genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))

    genre = db.relationship("Genre")

    def __repr__(self):
        return f"<User '{self.email.title()}'>"


class UserSchema(Schema):
    id = fields.Int()
    email = fields.Str()
    password = fields.Str()
    name = fields.Str()
    surname = fields.Str()
    favorite_genre_id = fields.Int()
