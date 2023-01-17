from .app import db, login_manager
from sqlalchemy import func
from flask_login import UserMixin, current_user
class User(db.Model, UserMixin):
    username = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(64))

    def __repr__(self):
        return "<User (%d)>" % (self.username )


    def get_id(self):
        return self.username

class Author(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    name = db.Column(db. String (100))
    def __repr__(self):
        return "<Author (%d) %s>" % (self.id , self.name)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key =True)
    price = db.Column(db.Float)
    title = db.Column(db.String)
    url = db.Column(db.String)
    img = db.Column(db.String)
    author_id = db.Column(db.Integer, db.ForeignKey ("author.id"))
    author = db.relationship("Author",
        backref=db.backref("books", lazy="dynamic"))

    def __repr__ (self ):
        return "<Book (%d) %s>" % (self.id , self.title)


class Commentaire(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    id_user = db.Column(db.String, db.ForeignKey("user.username"))
    user = db.relationship("User",
        backref=db.backref("users", lazy="dynamic"))
    id_book = db.Column(db.Integer, db.ForeignKey("book.id"))
    commentaire = db.Column(db.String)
    note = db.Column(db.Integer)


class Bibliotheque(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_user = db.Column(db.String, db.ForeignKey("user.username"))
    user = db.relationship("User",
                           backref=db.backref("fk_user_Bibliotheque", lazy="dynamic"))
    id_book = db.Column(db.Integer, db.ForeignKey("book.id"))
    #unique constraint between id, id_user and id_book
    __table_args__ = (db.UniqueConstraint('id_user', 'id_book', name='unique_id_user_id_book'),)

def get_sample():
    return Book.query.limit(10).all()

def get_all():
    return Book.query.all()

def get_prix(min, max):
    return Book.query.filter(Book.price >= min).filter(Book.price <= max).all()

def get_name(name):
    search = "%{}%".format(name)
    return Book.query.filter(Book.title.like(search)).all()

def get_author():
    return Author.query.order_by(Author.name.asc()).all()

def get_id_max():
    return db.session.query(func.max(Author.id)).scalar()

def get_author_by_id(id):
    return Author.query.filter(Author.id==id).all()

def get_book_author(name):
    return Author.query.filter(Author.name==name).one().books.all()

def get_autheur_existe(name):
    return Author.query.filter(Author.name==name).count() == 1

@login_manager.user_loader
def load_user(username):
    return User.query.get(username)

def get_books(id):

    x = Bibliotheque.query.filter(Bibliotheque.id_user == id).all()
    y = []
    for i in x:
        y.append(i.id_book)
    return Book.query.filter(Book.id.in_(y)).all()



def add_book(id_user, id_book):
    b = Bibliotheque (id_user=id_user, id_book=id_book)
    db.session.add(b)
    db.session.commit()

def del_book(id_user, id_book):
    b = Bibliotheque.query.filter(Bibliotheque.id_user==id_user).filter(Bibliotheque.id_book==id_book).one()
    db.session.delete(b)
    db.session.commit()


def inbibli(id):
    return Bibliotheque.query.filter(Bibliotheque.id_book == id).count() == 1

def inCom(id):
    return Commentaire.query.filter(Commentaire.id == id).count() == 1

def delCom(id):
    c = Commentaire.query.filter(Commentaire.id == id).one()
    db.session.delete(c)
    db.session.commit()

def get_one_commentaire(id, current_user):
    return Commentaire.query.filter(Commentaire.id_book==id).filter(Commentaire.id_user==current_user).one()
def get_commentaire(id):
    return Commentaire.query.filter(Commentaire.id_book==id).all()

def editCom(id, com, note):
    c = Commentaire.query.filter(Commentaire.id == id).one()
    c.commentaire = com
    c.note = note
    db.session.commit()

def hascomment(id):
    return Commentaire.query.filter(Commentaire.id_user==id).count() == 1
def get_id_commentaire_max():
    return db.session.query(func.max(Commentaire.id)).scalar()

def obtenir_par_recherche(contrainte):
    res = Book.query.join(Author)
    if contrainte.prix_mini.data != "":
        print(contrainte.prix_mini.data)
        res = res.filter(Book.price >= int(contrainte.prix_mini.data))
    if contrainte.prix_maxi.data != "":
        print(contrainte.prix_maxi.data)
        res = res.filter(Book.price <= int(contrainte.prix_maxi.data))
    if contrainte.nom_livre.data != "":
        search = "%{}%".format(contrainte.nom_livre.data)
        res = res.filter(Book.title.ilike(search))
    if contrainte.nom_auteur.data != "":
        search = "%{}%".format(contrainte.nom_auteur.data)
        res = res.filter(Author.name.ilike(search))
    return res.all()
