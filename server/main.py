from flask import Flask, jsonify, session, request
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, User, Book, Borrowing, Review
from datetime import datetime
from flask_marshmallow import Marshmallow
import bcrypt


app = Flask(__name__)
app.secret_key = 'ed976105693e2d6308ddf5dfe86eaa7d'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
CORS(app)
db.init_app(app)
ma = Marshmallow(app)


# Defining Marshmallow Schemas

class BookSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Book

    id = ma.auto_field()
    userID = ma.auto_field()
    title = ma.auto_field()
    author = ma.auto_field()
    publisher = ma.auto_field()
    publisheddate = ma.auto_field()
    duedate = ma.auto_field()
    image = ma.auto_field()
    description = ma.auto_field()


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User

    id = ma.auto_field()
    username = ma.auto_field()
    email = ma.auto_field()
    password = ma.auto_field()


class BorrowingSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Borrowing

    id = ma.auto_field()
    userID = ma.auto_field()
    bookID = ma.auto_field()
    borrowing_date = ma.auto_field()
    return_date = ma.auto_field()


class ReviewSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Review

    id = ma.auto_field()
    bookID = ma.auto_field()
    userID = ma.auto_field()
    rating = ma.auto_field()
    comment = ma.auto_field()


# Routes

@app.route('/')
def index():
    return {"message": "success"}


# Books Routes

@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    book_schema = BookSchema(many=True)
    book_data = book_schema.dump(books)
    return jsonify(book_data)


@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.filter_by(id=book_id).first()
    if book is None:
        return jsonify({'message': 'Book not found'}), 404

    book_schema = BookSchema()
    book_data = book_schema.dump(book)
    return jsonify(book_data)


@app.route('/books', methods=['POST'])
def create_book():
    data = request.get_json()

    book_schema = BookSchema()
    book = book_schema.load(data)

    new_book = Book(**book)

    db.session.add(new_book)
    db.session.commit()

    book_data = book_schema.dump(new_book)
    return jsonify(book_data), 201

@app.route('/books/<int:book_id>', methods=['PATCH'])
def update_book(book_id):
    data = request.get_json()

    book = Book.query.filter_by(id=book_id).first()
    if not book:
        return jsonify({'message': 'Book not found'}), 404

    book_schema = BookSchema()
    updated_book_data = book_schema.load(data, partial=True)

    book.title = updated_book_data.get('title', book.title)
    book.author = updated_book_data.get('author', book.author)
    book.publisher = updated_book_data.get('publisher', book.publisher)
    book.publisheddate = updated_book_data.get('publisheddate', book.publisheddate)
    book.duedate = updated_book_data.get('duedate', book.duedate)
    book.image = updated_book_data.get('image', book.image)
    book.description = updated_book_data.get('description', book.description)

    db.session.commit()

    book_data = book_schema.dump(book)
    return jsonify(book_data)


@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.filter_by(id=book_id).first()
    if not book:
        return jsonify({'message': 'Book not found'}), 404

    db.session.delete(book)
    db.session.commit()

    return jsonify({'message': 'Book deleted'}), 204


# Users Routes

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_schema = UserSchema(many=True)
    user_data = user_schema.dump(users)
    return jsonify(user_data)


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.filter_by(id=user_id).first()
     
    if user is None:
        return jsonify({'message': 'User not found'}), 404

    user_schema = UserSchema()
    user_data = user_schema.dump(user)
    return jsonify(user_data)


@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()

    user_schema = UserSchema()
    user = user_schema.load(data)
    
    new_user = User(**user)

    db.session.add(new_user)
    db.session.commit()

    user_data = user_schema.dump(new_user)
    return jsonify(user_data), 201


@app.route('/users/<int:user_id>', methods=['PATCH'])
def update_user(user_id):
    data = request.get_json()

    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({'message': 'user is been not found'}), 404

    user_schema = UserSchema()
    updated_user_data = user_schema.load(data, partial=True)

    user.username = updated_user_data.get('username', user.username)
    user.email = updated_user_data.get('email', user.email)
    user.password = updated_user_data.get('password', user.password)
    

    db.session.commit()

    user_data = user_schema.dump(user)
    return jsonify(user_data)



@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    
    if not user:
        return jsonify({'message': 'User not found'}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'User deleted'}), 204


# Borrowings Routes

@app.route('/borrowings', methods=['GET'])
def get_borrowings():
    borrowings = Borrowing.query.all()
    borrowing_schema = BorrowingSchema(many=True)
    borrowing_data = borrowing_schema.dump(borrowings)
    return jsonify(borrowing_data)


@app.route('/borrowings/<int:borrowing_id>', methods=['GET'])
def get_borrowing(borrowing_id):
    borrowing = Borrowing.query.filter_by(id=borrowing_id).first()
    if borrowing is None:
        return jsonify({'message': 'Borrowing not found'}), 404

    borrowing_schema = BorrowingSchema()
    borrowing_data = borrowing_schema.dump(borrowing)
    return jsonify(borrowing_data)


@app.route('/borrowings', methods=['POST'])
def create_borrowing():
    data = request.get_json()

    borrowing_schema = BorrowingSchema()
    borrowing = borrowing_schema.load(data)
    
    new_borrowing = Borrowing(**borrowing)

    db.session.add(new_borrowing)
    db.session.commit()

    borrowing_data = borrowing_schema.dump(new_borrowing)
    return jsonify(borrowing_data), 201


@app.route('/borrowings/<int:borrowing_id>', methods=['PATCH'])
def update_borrowing(borrowing_id):
    data = request.get_json()

    borrowing = Borrowing.query.filter_by(id=borrowing_id).first()
    if not borrowing:
        return jsonify({'message': 'borrowing has not  been found'}), 404

    borrowing_schema = BorrowingSchema()
    updated_borrowing_data = borrowing_schema.load(data, partial=True)

    borrowing.userID = updated_borrowing_data.get('userID', borrowing.userID)
    borrowing.bookID = updated_borrowing_data.get('bookID', borrowing.bookID)
    borrowing.borrowing_date = updated_borrowing_data.get('borrowing_date', borrowing.borrowing_date)
    borrowing.return_date = updated_borrowing_data.get('return_date', borrowing.return_date)
    

    db.session.commit()

    borrowing_data = borrowing_schema.dump(borrowing)
    return jsonify(borrowing_data)

@app.route('/borrowings/<int:borrowing_id>', methods=['DELETE'])
def delete_borrowing(borrowing_id):
    borrowing = Borrowing.query.filter_by(id=borrowing_id).first()
    if not borrowing:
        return jsonify({'message': 'Borrowing not found'}), 404

    db.session.delete(borrowing)
    db.session.commit()

    return jsonify({'message': 'Borrowing deleted'}), 204


# Reviews Routes

@app.route('/reviews', methods=['GET'])
def get_reviews():
    reviews = Review.query.all()
    review_schema = ReviewSchema(many=True)
    review_data = review_schema.dump(reviews)
    return jsonify(review_data)


@app.route('/reviews/<int:review_id>', methods=['GET'])
def get_review(review_id):
    review = Review.query.filter_by(id=review_id).first()
    if review is None:
        return jsonify({'message': 'Review not found'}), 404

    review_schema = ReviewSchema()
    review_data = review_schema.dump(review)
    return jsonify(review_data)


@app.route('/reviews', methods=['POST'])
def create_review():
    data = request.get_json()

    review_schema = ReviewSchema()
    review = review_schema.load(data)
    
    new_review = Review(**review)

    db.session.add(new_review)
    db.session.commit()

    review_data = review_schema.dump(new_review)
    return jsonify(review_data), 201

@app.route('/reviews/<int:review_id>', methods=['PATCH'])
def update_review(review_id):
    data = request.get_json()

    review = Review.query.filter_by(id=review_id).first()
    if not review:
        return jsonify({'message': 'review has not  been found'}), 404

    review_schema = ReviewSchema()
    updated_review_data = review_schema.load(data, partial=True)

    review.userID = updated_review_data.get('userID', review.userID)
    review.bookID = updated_review_data.get('bookID', review.bookID)
    review.rating = updated_review_data.get('rating', review.rating)
    review.comment = updated_review_data.get('comment', review.comment)
    

    db.session.commit()

    review_data = review_schema.dump(review)
    return jsonify(review_data)

@app.route('/reviews/<int:review_id>', methods=['DELETE'])
def delete_review(review_id):
    review = Review.query.filter_by(id=review_id).first()
    if not review:
        return jsonify({'message': 'Review not found'}), 404

    db.session.delete(review)
    db.session.commit()

    return jsonify({'message': 'Review deleted'}), 204

# LOGGING IN AND AUTHENTICATION

@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    email = request.json.get('email')

    # Hashing the password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    user = User(username=username, password=hashed_password, email=email)

    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully'})

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    user = authenticate_user(username, password)

    if user:
        session['user_id'] = user.id
        return jsonify({'message': 'Logged in successfully'})
    else:
        return jsonify({'message': 'Invalid username or password'}), 401

@app.route('/check_session')
def check_session():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        if user:
            return jsonify({'message': 'Session is active', 'user': user.username})
        else:
            
            session.pop('user_id', None)
            return jsonify({'message': 'Session is not active'}), 401
    else:
        return jsonify({'message': 'Session is not active'}), 401
    
@app.route('/logout')
def logout():
    user_id = session.get('user_id')
    if user_id:
        session.pop('user_id')
        return jsonify({'message': 'Logged out successfully'})
    else:
        return jsonify({'message': 'No active session'}), 401


# Helper function to authenticate the user
def authenticate_user(username, password):
    user = User.query.filter_by(username=username).first()
    if user and bcrypt.checkpw(password.encode('utf-8'), user.password):
        return user
    return None


if __name__ == '__main__':
    app.run(port=5555)
