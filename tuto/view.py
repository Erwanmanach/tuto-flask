from .app import app, db
from .models import *
from flask import render_template, url_for , redirect, request
from flask_wtf import FlaskForm
from flask_login import login_user, logout_user
from wtforms import StringField , HiddenField, PasswordField
from hashlib import sha256
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')

    def get_authenticated_user(self):
        user = User.query.get(self.username.data)
        if user is None:
            return None
        m = sha256()
        m.update(self.password.data.encode())
        passwd = m.hexdigest()
        return user if passwd == user.password else None

class AuthorForm(FlaskForm):
    id = HiddenField('id')
    name = StringField('Nom', validators =[DataRequired()])

@app.route ("/login/", methods =("GET","POST" ,))
def login():
    f = LoginForm()
    if f.validate_on_submit():
        user = f.get_authenticated_user()
        if user:
            login_user(user)
            return redirect(url_for("home"))
    return render_template(
            "login.html",
            form=f)

@app.route("/logout/")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/")
def home():
    return render_template(
            "home.html",
            title ="La selection du mois",
            books = get_sample()
    )

@app.route("/test")
def template2():
    print(22)
    return render_template(
            "templates2.html",
            title = "Les 100 meilleurs livres de SF",
            data = get_all())

@app.route("/test/search", methods=("GET",))
def research():
    return render_template(
            "templates2.html",
            title = "résultat pour " + str(request.args.get('search')),
            data = get_name(str(request.args.get('search'))))

@app.route("/test/<min>/<max>")
def recherche_prix(min,max):
    return render_template(
            "templates2.html",
            title = "Les livres entre "+ min +" et "+max,
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
        if not get_autheur_existe(f.name.data):
            if f.id.data == "":
                o = Author(name=f.name.data)
                db.session.add(o)
                db.session.commit()
                id = get_id_max()
            else:
                id = int(f.id.data)
                a = get_author_by_id(id)[0]
                a.name = f.name.data
                db.session.commit()
            return redirect( url_for("livre_auteur_id", idauteur=id))
    if f.id.data == "":
        a = dict()
        a["id"] = None
        a["name"] = f.name.data
    else:
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
    else:
        a = dict()
        a["name"] = ""
        a["id"] = None
        f = AuthorForm(id=a["id"], name=a["name"])
    return render_template(
            "edit-author.html",
            author=a, form=f)

