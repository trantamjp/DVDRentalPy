from sqlalchemy import Column, DateTime, ForeignKey, text
from sqlalchemy.orm import relationship

from app import db
from app.models.base_model import BaseModel


class FilmActor(db.Model, BaseModel):
    __tablename__ = 'film_actor'

    actor_id = Column(ForeignKey('actor.actor_id', ondelete='RESTRICT',
                                 onupdate='CASCADE'), primary_key=True, nullable=False)
    film_id = Column(ForeignKey('film.film_id', ondelete='RESTRICT',
                                onupdate='CASCADE'), primary_key=True, nullable=False, index=True)
    last_update = Column(DateTime, nullable=False,
                         server_default=text("now()"))

    actor = relationship('Actor', backref='film_actors')
    film = relationship('Film', backref='film_actors')

    def __repr__(self):
        return '<FilmActor film_id={} actor_id={}>'.format(self.film_id, self.actor_id)
