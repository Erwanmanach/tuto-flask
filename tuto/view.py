from .app import app
from .models import get_sample
from flask import render_template

@app.route("/")
def home():
    return render_template(
            "home.html",
            title ="My Books !",
            books = get_sample()
    )

@app.route("/test")
def template2():
    print(get_sample())
    return render_template(
            "templates2.html",
            title = "Les 10 meilleurs livres de SF",
            data = get_sample())

@app.route("/detail/<id>")
def detail(id):
    books = get_sample()
    book = books[int(id)]
    return render_template(
        "detail.html",
        book=book)