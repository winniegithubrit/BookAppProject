from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from datetime import datetime
from sqlalchemy.orm import validates
from marshmallow import Schema, fields

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)

    @validates("password")
    def validate_password(self, key, password):
        if password and len(password) < 15:
            raise ValueError('User password is not valid, please try again')
        return password

    borrowings = db.relationship('Borrowing', backref='user')
    reviews = db.relationship('Review', backref='user')


class Book(db.Model):
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


class Borrowing(db.Model):
    __tablename__ = 'borrowing'

    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.id'))
    bookID = db.Column(db.Integer, db.ForeignKey('book.id'))
    borrowing_date = db.Column(db.DateTime)
    return_date = db.Column(db.DateTime)


class Review(db.Model):
    __tablename__ = 'review'

    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.id'))
    bookID = db.Column(db.Integer, db.ForeignKey('book.id'))
    rating = db.Column(db.Integer)
    comment = db.Column(db.String)


class UserSchema(Schema):
    id = fields.Integer()
    username = fields.String()
    email = fields.String()
    password = fields.String()


class BookSchema(Schema):
    id = fields.Integer()
    userID = fields.Integer()
    title = fields.String()
    author = fields.String()
    publisher = fields.String()
    publisheddate = fields.DateTime()
    duedate = fields.DateTime()
    image = fields.String()
    description = fields.String()


class BorrowingSchema(Schema):
    id = fields.Integer()
    userID = fields.Integer()
    bookID = fields.Integer()
    borrowing_date = fields.DateTime()
    return_date = fields.DateTime()


class ReviewSchema(Schema):
    id = fields.Integer()
    userID = fields.Integer()
    bookID = fields.Integer()
    rating = fields.Integer()
    comment = fields.String()
