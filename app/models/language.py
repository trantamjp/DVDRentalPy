from sqlalchemy import Column, DateTime, Integer,  CHAR, text

from app import db
from app.models.base_model import BaseModel


class Language(db.Model, BaseModel):
    __tablename__ = 'language'

    language_id = Column(Integer, primary_key=True, server_default=text(
        "nextval('language_language_id_seq'::regclass)"))
    name = Column(CHAR(20), nullable=False)
    last_update = Column(DateTime, nullable=False,
                         server_default=text("now()"))

    def __repr__(self):
        return '<Language {} {}>'.format(self.language_id, self.name)
