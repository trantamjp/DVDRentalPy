from sqlalchemy import Column, DateTime, Integer, String, text
from sqlalchemy.orm import relationship

from app import db
from app.models.base_model import BaseModel
from app.models.film_actor import FilmActor


class Actor(db.Model, BaseModel):
    __tablename__ = 'actor'

    actor_id = Column(Integer, primary_key=True, server_default=text(
        "nextval('actor_actor_id_seq'::regclass)"))
    first_name = Column(String(45), nullable=False)
    last_name = Column(String(45), nullable=False, index=True)
    last_update = Column(DateTime, nullable=False,
                         server_default=text("now()"))

    films = relationship('Film', secondary='film_actor',
                         back_populates="actors")

    def __repr__(self):
        return '<Actor {} {} {}>'.format(self.actor_id, self.first_name, self.last_name)
