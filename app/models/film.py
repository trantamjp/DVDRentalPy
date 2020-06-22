from sqlalchemy import (ARRAY, Column, DateTime, Enum, ForeignKey, Integer,
                        Numeric, SmallInteger, String, Text, cast, or_, text)
from sqlalchemy.dialects.postgresql import TSVECTOR
from sqlalchemy.orm import joinedload, relationship

from app import db
from app.models.actor import Actor
from app.models.base_model import BaseModel
from app.models.category import Category
from app.models.film_category import FilmCategory
from app.models.language import Language

search_like_escape = BaseModel.search_like_escape


class Film(db.Model, BaseModel):
    __tablename__ = 'film'

    film_id = Column(Integer, primary_key=True, server_default=text(
        "nextval('film_film_id_seq'::regclass)"))
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text)
    release_year = Column(Integer)
    language_id = Column(ForeignKey('language.language_id',
                                    ondelete='RESTRICT', onupdate='CASCADE'), nullable=False, index=True)
    rental_duration = Column(
        SmallInteger, nullable=False, server_default=text("3"))
    rental_rate = Column(Numeric(4, 2), nullable=False,
                         server_default=text("4.99"))
    length = Column(SmallInteger)
    replacement_cost = Column(
        Numeric(5, 2), nullable=False, server_default=text("19.99"))
    rating = Column(Enum('G', 'PG', 'PG-13', 'R', 'NC-17',
                         name='mpaa_rating'), server_default=text("'G'::mpaa_rating"))
    last_update = Column(DateTime, nullable=False,
                         server_default=text("now()"))
    special_features = Column(ARRAY(Text()))
    fulltext = Column(TSVECTOR, nullable=False, index=True)

    language = relationship('Language')

    categories = relationship('Category', secondary='film_category',
                              back_populates="films")
    actors = relationship('Actor', secondary='film_actor',
                          back_populates="films")

    def __repr__(self):
        return '<Film {} {}>'.format(self.film_id, self.title)

    @classmethod
    def datatable_search(cls, args):

        start = args.get('start') or 0
        length = args.get('length') or 10
        orders = args.get('order') or []
        search = args.get('search') or {}
        columns = args.get('columns') or []

        records_total = Film.query.count()

        rs_filtered = Film.query

        for filter_name in ['title', 'description', 'rating', 'rental_rate', 'length', 'language', 'categories', 'actors']:
            column = next(
                (col for col in columns if col.get('name') == filter_name), None)
            if column == None:
                continue

            search_value = column.get('search').get('value') or ''
            if search_value == '':
                continue

            if filter_name == 'title':
                rs_filtered = rs_filtered.filter(
                    Film.title.ilike(search_like_escape(search_value)))
                continue

            if filter_name == 'description':
                rs_filtered = rs_filtered.filter(
                    Film.description.ilike(search_like_escape(search_value)))
                continue

            if filter_name == 'rating':
                rs_filtered = rs_filtered.filter(Film.rating == search_value)
                continue

            if filter_name == 'rental_rate':
                rs_filtered = rs_filtered.filter(
                    cast(Film.rental_rate, Text).ilike(
                        search_like_escape(search_value))
                )
                continue

            if filter_name == 'length':
                rs_filtered = rs_filtered.filter(
                    cast(Film.length, Text).ilike(
                        search_like_escape(search_value))
                )
                continue

            if filter_name == 'language':
                rs_filtered = rs_filtered.filter(
                    Film.language.has(Language.language_id == search_value)
                )
                continue

            if filter_name == 'categories':
                rs_filtered = rs_filtered.filter(
                    Film.categories.any(Category.category_id == search_value)
                )
                continue

            if filter_name == 'actors':
                search_value_like = search_like_escape(search_value)
                rs_filtered = rs_filtered.filter(
                    Film.actors.any(or_(
                        Actor.first_name.ilike(search_value_like),
                        Actor.last_name.ilike(search_value_like),
                    ))
                )
                continue

        records_filtered = rs_filtered.count()

        rs_filtered_ordered = rs_filtered.join(Language)

        for order in orders:
            order_column = columns[order.get('column')].get('name')
            if order_column == 'language':
                cls_attr = Language.name
            else:
                cls_attr = getattr(Film, order_column)

            rs_filtered_ordered = rs_filtered_ordered.order_by(
                cls_attr.desc() if order.get('dir') == 'desc' else cls_attr.asc())

        films = rs_filtered_ordered.options(joinedload(Film.language),
                                            joinedload(Film.categories),
                                            joinedload(Film.actors)) \
            .offset(start).limit(length).all()

        film_list = {
            'records_total': records_total,
            'records_filtered': records_filtered,
            'films': films,
        }

        return film_list
