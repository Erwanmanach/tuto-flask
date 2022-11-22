from .app import app
from .models import get_sample, get_all
from flask import render_template

@app.route("/")
def home():
    return render_template(
            "home.html",
            title ="La selection du mois",
            books = get_sample()
    )

@app.route("/test")
def template2():
    return render_template(
            "templates2.html",
            title = "Les 10 meilleurs livres de SF",
            data = get_all())

@app.route("/detail/<id>")
def detail(id):
    books = get_all()
    book = books[int(id)]
    return render_template(
        "detail.html",
        book=book)