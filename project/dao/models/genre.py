from marshmallow import Schema, fields

from project.dao.models.base import BaseMixin
from project.setup_db import db


class Genre(BaseMixin, db.Model):
    __tablename__ = "genre"

    name = db.Column(db.String(100), unique=True, nullable=False)

    def __repr__(self):
        return f"<Genre '{self.name.title()}'>"

class GenreSchema(Schema):
    id = fields.Int()
    name = fields.Str()

