from .app import db

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

def get_sample():
    return Book.query.limit(10).all()

def get_all():
    return Book.query.all()

def get_prix(min, max):
    return Book.query.filter(Book.price >= min).filter(Book.price <= max).all()

def get_author():
    return Author.query.all()

def get_author_by_id(id):
    return Author.query.filter(Author.id==id).all()

def get_book_author(name):
    return Author.query.filter(Author.name==name).one().books.all()