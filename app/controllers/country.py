from flask import jsonify, request

from app.model_factory import ModelFactory


def get_countries():
    rows = ModelFactory.country.query.order_by(
        ModelFactory.country.country.asc()).all()
    countries = list(map(lambda row: row.row2dict(), rows))
    return jsonify(countries)
