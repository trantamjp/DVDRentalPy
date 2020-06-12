import json

from flask import flash, jsonify, redirect, render_template, request, url_for
from sqlalchemy import func, or_

from app import app
from app.controlers.customer import Customer as CustomerController
from app.controlers.film import Film as FilmController


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/customers")
def customers():
    return render_template("customers.html")


@app.route("/films")
def films():
    return render_template("films.html")


@app.route('/api/customers', methods=["GET", "POST"])
def api_customers():
    args = request.values.get("args")
    if args:
        args = json.loads(args)
    else:
        args = {}

    response = CustomerController.datatable_search(args)
    return jsonify(response)


@app.route('/api/films', methods=["GET", "POST"])
def api_films():
    args = request.values.get("args")
    if args:
        args = json.loads(args)
    else:
        args = {}

    response = FilmController.datatable_search(args)
    return jsonify(response)
