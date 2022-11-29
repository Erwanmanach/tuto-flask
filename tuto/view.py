from .app import app, db
from .models import *
from flask import render_template, url_for , redirect
from flask_wtf import FlaskForm
from wtforms import StringField , HiddenField
from wtforms.validators import DataRequired

class AuthorForm(FlaskForm):
    id = HiddenField ('id')
    name = StringField ('Nom', validators =[ DataRequired ()])

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

@app.route("/save/author/", methods=("POST",))
def save_author():
    a = None
    f = AuthorForm ()
    if f.validate_on_submit ():
        id = int(f.id.data)
        a = get_author_by_id(id)[0]
        a.name = f.name.data
        db.session.commit()
        return redirect( url_for("livre_auteur_id", idauteur=a.id))
    a = get_author(int(f.id.data))
    return render_template (
        "edit-author.html",
        author=a, form=f)

@app.route("/author")
def auteur():
    return render_template(
        "author.html",
        auteurs=get_author()
    )

@app.route("/author/<string:name>")
def livre_auteur_name(name):
    return render_template(
        "livre_auteur.html",
        title = "livre écrit par " + name,
        books = get_book_author(""+name)
    )

@app.route("/author/<int:idauteur>")
def livre_auteur_id(idauteur):
    nom = get_author_by_id(idauteur)[0].name
    return render_template(
        "livre_auteur.html",
        title = "livre écrit par " + nom,
        books = get_book_author("" + nom)
    )


@app.route("/edit/author/<int:id>")
def edit_author(id):
    a = get_author_by_id(id)
    if len(a) != 0:
        a = a[0]
        f = AuthorForm(id=a.id, name=a.name)
        return render_template(
                "edit-author.html",
                author=a, form=f)
    else:
        
