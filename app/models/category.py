from sqlalchemy import Column, DateTime, Integer, String, text
from sqlalchemy.orm import relationship

from app import db
from app.models.base_model import BaseModel
from app.models.film_category import FilmCategory


class Category(db.Model, BaseModel):
    __tablename__ = 'category'

    category_id = Column(Integer, primary_key=True, server_default=text(
        "nextval('category_category_id_seq'::regclass)"))
    name = Column(String(25), nullable=False)
    last_update = Column(DateTime, nullable=False,
                         server_default=text("now()"))

    films = relationship('Film', secondary='film_category',
                         back_populates="categories")

    def __repr__(self):
        return '<Category {} {}>'.format(self.category_id, self.name)
