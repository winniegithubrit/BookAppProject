from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import func
from datetime import datetime

db = SQLAlchemy()


class User(db.Model, SerializerMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)
    

    borrowings = db.relationship('Borrowing', backref='user')
    reviews = db.relationship('Review', backref='user')


class Book(db.Model, SerializerMixin):
    __tablename__ = 'book'

    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String)
    author = db.Column(db.String)
    publisher = db.Column(db.String)
    publisheddate = db.Column(db.DateTime, default=func.now())
    duedate = db.Column(db.DateTime)
    image = db.Column(db.String)
    description = db.Column(db.String)

    borrowings = db.relationship('Borrowing', backref='book')
    reviews = db.relationship('Review', backref='book')


class Borrowing(db.Model, SerializerMixin):
    __tablename__ = 'borrowing'

    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.id'))
    bookID = db.Column(db.Integer, db.ForeignKey('book.id'))
    borrowing_date = db.Column(db.DateTime)
    return_date = db.Column(db.DateTime)


class Review(db.Model, SerializerMixin):
    __tablename__ = 'review'

    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.id'))
    bookID = db.Column(db.Integer, db.ForeignKey('book.id'))
    rating = db.Column(db.Integer)
    comment = db.Column(db.String)
