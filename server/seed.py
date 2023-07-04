from faker import Faker
import random
from datetime import datetime
from models import db, Book, User, Borrowing, Review
from main import app

fake = Faker()

with app.app_context():
    db.drop_all()
    db.create_all()

    users = []
    for i in range(10):
        firstname = fake.first_name()
        lastname = fake.last_name()
        contact_info = fake.address()
        email = fake.email()
        phone_number = fake.phone_number()

        user = User(
            firstname=firstname,
            lastname=lastname,
            contactInfo=contact_info,
            email=email,
            phone_number=phone_number
        )
        users.append(user)

    db.session.bulk_save_objects(users)
    db.session.commit()

    books = []
    for i in range(30):
        user_id = random.randint(1, 10)
        title = fake.sentence(nb_words=3)
        author = fake.name()
        publisher = fake.company()
        publisheddate = fake.date_time_between(start_date='-5y', end_date='now')
        duedate = fake.date_between(start_date='+30d', end_date='+60d')
        image = fake.image_url()
        description = fake.text()

        book = Book(
            userID=user_id,
            title=title,
            author=author,
            publisher=publisher,
            publisheddate=publisheddate,
            duedate=duedate,
            image=image,
            description=description
        )
        books.append(book)

    db.session.bulk_save_objects(books)
    db.session.commit()

    borrowings = []
    for i in range(30):
        user_id = random.randint(1, 10)
        book_id = random.randint(1, 30)
        
        borrowing_date = fake.date_time_between(start_date='-30d', end_date='-1d')
        return_date = fake.date_time_between(start_date='now', end_date='+30d')

        borrowing = Borrowing(
            userID=user_id,
            bookID=book_id,
            borrowing_date=borrowing_date,
            return_date=return_date
        )
        borrowings.append(borrowing)

    db.session.bulk_save_objects(borrowings)
    db.session.commit()
    
    reviews = []
    for i in range(30):
        user_id = random.randint(1, 10)
        book_id = random.randint(1, 30)
        rating = random.randint(1, 5)
        comment = fake.paragraph()
      
        review = Review(
            userID=user_id,
            bookID=book_id,
            rating=rating,
            comment=comment
        )
        reviews.append(review)
      
    db.session.bulk_save_objects(reviews)
    db.session.commit()
