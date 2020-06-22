from sqlalchemy import Column, DateTime, ForeignKey, text
from sqlalchemy.orm import relationship

from app import db
from app.models.base_model import BaseModel


class FilmCategory(db.Model, BaseModel):
    __tablename__ = 'film_category'

    film_id = Column(ForeignKey('film.film_id', ondelete='RESTRICT',
                                onupdate='CASCADE'), primary_key=True, nullable=False)
    category_id = Column(ForeignKey('category.category_id', ondelete='RESTRICT',
                                    onupdate='CASCADE'), primary_key=True, nullable=False)
    last_update = Column(DateTime, nullable=False,
                         server_default=text("now()"))

    category = relationship('Category', backref='film_categories')
    film = relationship('Film', backref='film_categories')

    def __repr__(self):
        return '<FilmCategory film_id={} category_id={}>'.format(self.film_id, self.category_id)
