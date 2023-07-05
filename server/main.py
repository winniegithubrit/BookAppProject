from flask import Flask, jsonify, session, request
from flask_cors import CORS
from flask_migrate import Migrate
from models import db, User, Book, Borrowing, Review
from datetime import datetime
from flask_marshmallow import Marshmallow

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

    db.session.add(book)
    db.session.commit()

    book_data = book_schema.dump(book)
    return jsonify(book_data), 201


@app.route('/books/<int:book_id>', methods=['PATCH'])
def update_book(book_id):
    data = request.get_json()
    
    book = Book.query.filter_by(id=book_id).first()
    if not book:
        return jsonify({'message': 'Book not found'}), 404

    book_schema = BookSchema()
    book = book_schema.load(data, instance=book, partial=True)

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

    db.session.add(user)
    db.session.commit()

    user_data = user_schema.dump(user)
    return jsonify(user_data), 201


@app.route('/users/<int:user_id>', methods=['PATCH'])
def update_user(user_id):
    data = request.get_json()

    user = User.query.filter_by(id=user_id).first()

    if not user:
        return jsonify({'message': 'User not found'}), 404

    user_schema = UserSchema()
    user = user_schema.load(data, instance=user, partial=True)

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

    db.session.add(borrowing)
    db.session.commit()

    borrowing_data = borrowing_schema.dump(borrowing)
    return jsonify(borrowing_data), 201


@app.route('/borrowings/<int:borrowing_id>', methods=['PATCH'])
def update_borrowing(borrowing_id):
    data = request.get_json()

    borrowing = Borrowing.query.filter_by(id=borrowing_id).first()
    if not borrowing:
        return jsonify({'message': 'Borrowing not found'}), 404

    borrowing_schema = BorrowingSchema()
    borrowing = borrowing_schema.load(data, instance=borrowing, partial=True)

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

    db.session.add(review)
    db.session.commit()

    review_data = review_schema.dump(review)
    return jsonify(review_data), 201


@app.route('/reviews/<int:review_id>', methods=['PATCH'])
def update_review(review_id):
    data = request.get_json()

    review = Review.query.filter_by(id=review_id).first()
    if not review:
        return jsonify({'message': 'Review not found'}), 404

    review_schema = ReviewSchema()
    review = review_schema.load(data, instance=review, partial=True)

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

# LOGGING AND AUTHENTICATING THE USERS

@app.route('/register', methods=['POST'])
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    email = request.json.get('email')
    
    user = User(username=username, password=password, email=email)

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
# its using the get method also the check session 
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return jsonify({'message': 'Logged out successfully'})

@app.route('/check_session')
def check_session():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        return jsonify({'message': 'Session is active', 'user': user.username})
    else:
        return jsonify({'message': 'Session is not active'}), 401

# Helper function to authenticate the user
def authenticate_user(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.password == password:
        return user
    return None

if __name__ == '__main__':
    app.run(port=5555)
