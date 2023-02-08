from .app import app, db
from .models import *
from flask import render_template, url_for, redirect, request, flash
from flask_wtf import FlaskForm
from flask_login import login_user, logout_user, current_user
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
        print(passwd)
        print(user.password)
        return user if passwd == user.password else None


class RegisterForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')

    def get_authenticated_user(self):
        user = User.query.get(self.username.data)
        if user is None:
            return False
        else:
            return True

    def add_user(self):
        passwd = sha256(self.password.data.encode()).hexdigest()
        user = User(username=self.username.data, password=passwd,author_id = None)
        db.session.add(user)
        db.session.commit()



class AuthorForm(FlaskForm):
    id = HiddenField('id')
    name = StringField('Nom', validators =[DataRequired()])

class CommentaireForm(FlaskForm):
    pass

class Recherche(FlaskForm):
    search = StringField('search')

class RechercheForm(FlaskForm):
    prix_mini = StringField('prixmini')
    prix_maxi = StringField('Prixmaxi')
    nom_livre = StringField('Nomlivre')
    nom_auteur = StringField('NomAuteur')

    def est_vide(this):
        print(this.prix_maxi.data)
        return this.prix_maxi.data is None and this.prix_mini.data is None

@app.route("/")
def home():
    return render_template(
            "home.html",
            title ="La selection du mois",
            books = get_sample()
    )

@app.route("/login/", methods =("GET","POST" ,))
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

@app.route("/detail/<id>")
def detail(id):
    book = Book.query.get_or_404(id)
    commentaire = get_commentaire(id)
    username = ""
    if current_user.is_authenticated:
        username = current_user.username

    return render_template(
        "detail.html",
        book=book,
        commentaire=commentaire, inbibli=inbibli(id),hascomment=hascomment(username))

@app.route("/ajouteCommentaire/<id>", methods=("POST",))
def ajoute_commentaire(id):
    result = request.form

    if result["commentaire"] != "":
        o = Commentaire(id_user=current_user.username,id_book=id,commentaire=result["commentaire"], note=result["note"])
        db.session.add(o)
        db.session.commit()
    return redirect(url_for("detail",id=id))

@app.route("/delcom/<id>")
def delcom(id):
    idb = get_one_commentaire(id,current_user.username).id_book
    iscomowner = current_user.username == get_one_commentaire(id, current_user.username).id_user
    if iscomowner:
        if inCom(id):
            delCom(id)
    return redirect(url_for("detail",id=idb))

@app.route("/editcom/<id>", methods=("POST",))
def editcom(id):
    result = request.form
    idb = get_one_commentaire(id, current_user.username).id_book
    iscomowner = current_user.username == get_one_commentaire(id,current_user.username).id_user
    if iscomowner:
        if inCom(id):
            editCom(id,result["commentaire"],result["note"])
    return redirect(url_for("detail",id=idb))


@app.route("/test", methods=("GET","POST",))
def template2():
    result = RechercheForm()
    return render_template(
            "templates2.html",
            title = "Les 100 meilleurs livres de SF",
            data = get_all(),
            form = result)

@app.route("/research/nav", methods=("GET","POST",))
def researchnav():
    resultat = Recherche()
    print(resultat.search)
    result = RechercheForm()
    return render_template(
            "templates2.html",
            title = "résultat pour " + resultat["search"].data,
            data = get_name(resultat["search"].data),
            form = result
    )

@app.route("/test/search", methods=("GET","POST",))
def research():
    result = RechercheForm()
    return render_template(
            "templates2.html",
            title = "résultat pour " + result["search"],
            data = get_name(result["search"]),
            form = result)

@app.route("/research/prix", methods=("POST","GET"))
def lance_recherche():
    result = RechercheForm()
    if result.validate_on_submit():
        return render_template("templates2.html",
                    title = "recherche", data = obtenir_par_recherche(result),
                    form = result)
    return redirect(url_for("template2"))
    

@app.route("/test/<min>/<max>")
def recherche_prix(min,max):
    return render_template(
            "templates2.html",
            title = "Les livres entre "+ min +" et "+max +" euros",
            data = get_prix(min, max))


@app.route("/save/author/", methods=("POST",))
def save_author():
    a = None
    f = AuthorForm()
    if f.validate_on_submit():
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

@app.route("/biblio")
def biblio():
    return render_template(
        "biblio.html",
        title="Ma bibliothèque",
        books=get_books(current_user.username)
    )

@app.route("/home/<int:id>")
def addbook(id):
    if (not inbibli(id)):
        add_book(current_user.username, id)
        flash("Le livre a été ajouté à votre bibliothèque")
    else:
        flash("Le livre est déjà dans votre bibliothèque")

    return render_template(
        "home.html",
        title="La selection du mois",
        books=get_sample()
    )

@app.route("/biblio/<int:id>")
def deletebook(id):
    if (inbibli(id)):
        del_book(current_user.username, id)
        redirect (url_for("biblio"))
    return render_template(
        "biblio.html",
        title="Ma bibliothèque",
        books=get_books(current_user.username))


@app.route("/register/", methods =("GET","POST" ,))
def register():
    f = RegisterForm()
    if f.validate_on_submit():
        user = f.get_authenticated_user()
        if user:
            login_user(user)
        else:
            f.add_user()

        return redirect(url_for("home"))
    return render_template(
        "register.html",
        form=f)