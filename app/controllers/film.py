import json

from flask import jsonify, request

from app.model_factory import ModelFactory


def datatable_search():
    args = request.json if request.is_json else {}

    data = ModelFactory.film.datatable_search(args)

    films = []
    for film in data['films']:
        film_dict = film.row2dict()
        film_dict['language'] = film.language.row2dict()
        film_dict['categories'] = [category.row2dict()
                                   for category in film.categories]
        film_dict['actors'] = [actor.row2dict() for actor in film.actors]
        films.append(film_dict)

    response = {
        'draw':  args.get('draw'),
        'recordsTotal': data['records_total'],
        'recordsFiltered': data['records_filtered'],
        'data': films,
    }
    return jsonify(response)
