from .app import db, login_manager
from sqlalchemy import func
from flask_login import UserMixin

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
    return Author.query.all()

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
    return Book.query.filter(Book.id==Commentaire.id_book & Commentaire.id_user == id).all()

def get_commentaire(id):
    return Commentaire.query.filter(Commentaire.id_book==id).all()

def get_id_commentaire_max():
    return db.session.query(func.max(Commentaire.id)).scalar()