from flask import Flask,jsonify
from flask_migrate import Migrate
from flask import request, jsonify
from models import db,User,Book,Borrowing,Review
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate  = Migrate(app,db)
db.init_app(app)


@app.route('/')
def index():
  return {"message":"success"}
# all the books functionality
@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    book_list = []
    for book in books:
        book_data = {
            'id': book.id,
            'userID': book.userID,
            'title': book.title,
            'author': book.author,
            'publisher': book.publisher,
            'publisheddate': book.publisheddate,
            'duedate': book.duedate,
            'image': book.image,
            'description': book.description
        }
        book_list.append(book_data)
    
    return jsonify(book_list)
  
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.filter_by(id=book_id).first()
    if book is None:
        return jsonify({'message': 'Book has not been  found'})

    book_data = {
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'publisher': book.publisher,
        'publisheddate': book.publisheddate,
        'duedate': book.duedate,
        'image': book.image,
        'description': book.description
    }

    return jsonify(book_data)
  
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.filter_by(id=book_id).first()
    print(book)
    if book is None:
        return jsonify({'message': 'Book  is not found'})

    db.session.delete(book)
    db.session.commit()

    return jsonify({'message': 'Book has been deleted successfully'})


from flask import request, jsonify

@app.route('/books', methods=['POST'])
def create_book():
    data = request.get_json()

    
    title = data.get('title')
    author = data.get('author')
    publisher = data.get('publisher')
    published_date = data.get('published_date')
    due_date = data.get('due_date')
    image = data.get('image')
    description = data.get('description')

    
    book = Book(
        title=title,
        author=author,
        publisher=publisher,
        publisheddate=published_date,
        duedate=due_date,
        image=image,
        description=description
    )

    
    db.session.add(book)
    db.session.commit()

    
    response = {
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'publisher': book.publisher,
        'published_date': book.publisheddate,
        'due_date': book.duedate,
        'image': book.image,
        'description': book.description
    }

    return jsonify(response), 201



@app.route('/books/<int:book_id>', methods=['PATCH'])
def update_book(book_id):
    data = request.get_json()

    book = Book.query.filter_by(id=book_id).first()
    if not book:
        return jsonify({'message': 'Book not found'}), 404

    if 'title' in data:
        book.title = data['title']
    if 'author' in data:
        book.author = data['author']
    if 'publisher' in data:
        book.publisher = data['publisher']
    if 'published_date' in data:
        book.publisheddate = data['published_date']
    if 'due_date' in data:
        book.duedate = data['due_date']
    if 'image' in data:
        book.image = data['image']
    if 'description' in data:
        book.description = data['description']

    db.session.commit()

    response = {
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'publisher': book.publisher,
        'published_date': book.publisheddate,
        'due_date': book.duedate,
        'image': book.image,
        'description': book.description
    }

    return jsonify(response), 200

@app.route('/books/<int:book_id>', methods=['PUT'])
def updating_whole_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({'message': 'Book not found'})

    data = request.get_json()
    book.title = data.get('title')
    book.author = data.get('author')
    book.publisher = data.get('publisher')
    book.publisheddate = datetime.strptime(data.get('publisheddate'), '%Y-%m-%d %H:%M:%S.%f')
    book.duedate = datetime.strptime(data.get('duedate'), '%Y-%m-%d %H:%M:%S.%f')
    book.image = data.get('image')
    book.description = data.get('description')

    db.session.commit()

    return jsonify({'message': 'Book updated successfully'})

  
  
# users functionality

@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()

    user_list = []
    for user in users:
        user_data = {
            'id': user.id,
            'firstname': user.firstname,
            'lastname': user.lastname,
            'contactInfo': user.contactInfo,
            'email': user.email,
            'phone_number': user.phone_number,
            
        }
        user_list.append(user_data)

    return jsonify(user_list)
  
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user_by_id(user_id):
    user = User.query.filter_by(id=user_id).first()

    if user is None:
        return jsonify({'message': 'User not found'}), 404

    user_data = {
        'id': user.id,
        'firstname': user.firstname,
        'lastname': user.lastname,
        'contactInfo': user.contactInfo,
        'email': user.email,
        'phone_number': user.phone_number,
      
    }

    return jsonify(user_data)
  
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()

    firstname = data.get('firstname')
    lastname = data.get('lastname')
    contactInfo = data.get('contactInfo')
    email = data.get('email')
    phone_number = data.get('phone_number')

  

    user = User(firstname=firstname, lastname=lastname, contactInfo=contactInfo, email=email, phone_number=phone_number)
    db.session.add(user)
    db.session.commit()

    return jsonify({'message': 'User created successfully', 'user_id': user.id}), 201
  
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.filter(User.id == user_id).first()

    if not user:
        return jsonify({'message': 'User not found'}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'User deleted successfully'}), 200

# borrowing functionality

@app.route('/borrowings', methods=['GET'])
def get_borrowings():
    borrowings = Borrowing.query.all()
    borrowing_list = []
    for borrowing in borrowings:
        borrowing_dict = {
            'id': borrowing.id,
            'userID': borrowing.userID,
            'bookID': borrowing.bookID,
            'borrowing_date': borrowing.borrowing_date.strftime('%Y-%m-%d %H:%M:%S'),
            'return_date': borrowing.return_date.strftime('%Y-%m-%d %H:%M:%S')
        }
        borrowing_list.append(borrowing_dict)
    return jsonify(borrowing_list)

@app.route('/borrowings/<borrowing_id>', methods=['GET'])
def get_borrowing(borrowing_id):
    borrowing = Borrowing.query.filter_by(id=borrowing_id).first()

    if borrowing is not None:
        borrowing_data = {
            'id': borrowing.id,
            'userID': borrowing.userID,
            'bookID': borrowing.bookID,
            'borrowing_date': borrowing.borrowing_date,
            'return_date': borrowing.return_date
        }
        return jsonify(borrowing_data)
    else:
        return jsonify({'message': 'Borrowing not found.'}), 404

@app.route('/borrowings/<borrowing_id>', methods=['DELETE'])
def delete_borrowing(borrowing_id):
    borrowing = Borrowing.query.filter_by(id=borrowing_id).first()

    if borrowing is not None:
        db.session.delete(borrowing)
        db.session.commit()
        return jsonify({'message': 'Borrowing deleted successfully.'})
    else:
        return jsonify({'message': 'Borrowing not found.'}), 404


@app.route('/borrowings', methods=['POST'])
def create_borrowing():
    data = request.get_json()
    user_id = data.get('userID')
    book_id = data.get('bookID')

    new_borrowing = Borrowing(userID=user_id, bookID=book_id, borrowing_date=datetime.now())
    db.session.add(new_borrowing)
    db.session.commit()

    return jsonify({'message': 'Borrowing created successfully'})


if __name__ == '__main__':
    app.run(port=5555)
