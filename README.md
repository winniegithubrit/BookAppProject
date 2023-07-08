# Book App Backend

The backend of the Book App is built with Flask, a micro web framework for Python. It provides a set of API endpoints to perform CRUD (Create, Read, Update, Delete) operations on books, users, borrowings, and reviews. The backend also handles user authentication using bcrypt for password hashing and session management.

## Technologies Used

- Flask: A micro web framework for Python.
- SQLAlchemy: A Python SQL toolkit and Object-Relational Mapping (ORM) library.
- Flask-Migrate: A Flask extension for handling database migrations.
- Flask-CORS: A Flask extension for handling Cross-Origin Resource Sharing (CORS).
- Flask-Marshmallow: A Flask extension for object serialization/deserialization (marshalling).

## Folder Structure

The backend folder structure follows a typical Flask project structure:

- `models.py`: Defines the database models using SQLAlchemy.
- `main.py`: The main Flask application file containing API endpoints and configurations.
- `migrations/`: Contains database migration files.
- `requirements.txt`: Lists the Python dependencies required to run the backend.

## API Endpoints

### Books

- `GET /books`: Retrieve a list of all books.
- `GET /books/<book_id>`: Retrieve details of a specific book by ID.
- `POST /books`: Add a new book to the database.
- `PATCH /books/<book_id>`: Update an existing book by ID.
- `DELETE /books/<book_id>`: Delete a book by ID.

### Users

- `GET /users`: Retrieve a list of all users.
- `GET /users/<user_id>`: Retrieve details of a specific user by ID.
- `POST /users`: Register a new user.
- `PATCH /users/<user_id>`: Update an existing user by ID.
- `DELETE /users/<user_id>`: Delete a user by ID.

### Borrowings

- `GET /borrowings`: Retrieve a list of all borrowings.
- `GET /borrowings/<borrowing_id>`: Retrieve details of a specific borrowing by ID.
- `POST /borrowings`: Create a new borrowing.
- `PATCH /borrowings/<borrowing_id>`: Update an existing borrowing by ID.
- `DELETE /borrowings/<borrowing_id>`: Delete a borrowing by ID.

### Reviews

- `GET /reviews`: Retrieve a list of all reviews.
- `GET /reviews/<review_id>`: Retrieve details of a specific review by ID.
- `POST /reviews`: Create a new review.
- `PATCH /reviews/<review_id>`: Update an existing review by ID.
- `DELETE /reviews/<review_id>`: Delete a review by ID.

### User Authentication

- `POST /register`: Register a new user with username, password, and email.
- `POST /login`: Authenticate the user and generate a session token.
- `GET /check_session`: Check the status of the user session.
- `GET /logout`: Log out the user and invalidate the session.

## Database

The backend uses SQLite as the database .

# link to the frontend github repo
https://github.com/winniegithubrit/frontend-bookapp.git
