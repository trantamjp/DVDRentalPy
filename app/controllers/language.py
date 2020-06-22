from flask import jsonify, request

from app.model_factory import ModelFactory


def get_languages():
    rows = ModelFactory.language.query.order_by(
        ModelFactory.language.name.asc()).all()
    languages = list(map(lambda row: row.row2dict(), rows))
    return jsonify(languages)
