from .app import app
from .models import get_sample, get_all,get_author, get_book_author,get_prix, Book
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
            title = "Les 100 meilleurs livres de SF",
            data = get_all())

@app.route("/test/<min>/<max>")
def template(min,max):
    return render_template(
            "templates2.html",
            title = "Les 100 meilleurs livres de SF",
            data = get_prix(min, max))

@app.route("/detail/<id>")
def detail(id):
    book = Book.query.get_or_404(id)
    return render_template(
        "detail.html",
        book=book)

@app.route("/author")
def auteur():
    return render_template(
        "author.html",
        auteurs=get_author()
    )

@app.route("/author/<name>")
def livre_auteur(name):
    return render_template(
        "livre_auteur.html",
        title = "livre écrit par " + name,
        books = get_book_author(""+name)
    )