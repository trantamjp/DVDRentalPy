from urllib.parse import urlparse

from flask import redirect, render_template, request

from app import app
from app.controllers import category, country, customer, film, language


@app.route("/")
def index():
    base_url = urlparse(request.base_url)
    return redirect(base_url.scheme + '://' + base_url.hostname)


@app.route("/api/countries")
def api_countries():
    return country.get_countries()


@app.route("/api/datatable/customers", methods=["GET", "POST"])
def api_datatable_customers():
    return customer.datatable_search()


@app.route("/api/categories")
def api_categories():
    return category.get_categories()


@app.route("/api/languages")
def api_languages():
    return language.get_languages()


@app.route("/api/datatable/films", methods=["GET", "POST"])
def api_datatable_films():
    return film.datatable_search()


@app.route("/customers")
def customers():
    return render_template("customers.pug", title='Customers')


@app.route("/films")
def films():
    return render_template("films.pug", title='Films')


@app.route("/home")
def home():
    return render_template("home.pug")
