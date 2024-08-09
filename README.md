# Book Recommendation System (BRS)

## Overview

The Book Recommendation System (BRS) is a Django-based web application designed to help users discover and manage books. It integrates with the Google Books API to fetch book data and allows users to add their own books, set preferences, and get personalized book recommendations based on their interests.

## Features

- **User Authentication**: Secure login and signup features.
- **Personalized Recommendations**: Get book recommendations based on user preferences.
- **Book Management**: Add and view personal books.
- **Search Functionality**: Search for books using various filters like genre, author, rating, and more.
- **Category Preferences**: Update and manage book genre preferences.
- **Responsive Design**: User-friendly interface with responsive design for different devices.

## Technology Stack

- **Backend**: Django, Django REST Framework
- **Frontend**: HTML, CSS, Tailwind CSS
- **Database**: SQLite (or another database of your choice)
- **APIs**: Google Books API

## Setup

### Prerequisites

- Python 3.x
- Django
- Django REST Framework
- Requests library

### Installation

1. **Clone the repository:**

    ```bash
    git clone <repository-url>
    cd <project-directory>
    ```

2. **Create a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables:**

    Create a `.env` file in the root directory and add the following:

    ```
    GOOGLE_BOOKS_API_KEY=<your-google-books-api-key>
    ```

5. **Apply migrations:**

    ```bash
    python manage.py migrate
    ```

6. **Create a superuser (for admin access):**

    ```bash
    python manage.py createsuperuser
    ```

7. **Run the development server:**

    ```bash
    python manage.py runserver
    ```

8. **Visit the application:**

    Open your web browser and go to `http://127.0.0.1:8000/`.

## API Endpoints

### Authentication

- **Sign Up**
  - `POST /api/signup/`
  - Request Body: `{ "fname": "string", "lname": "string", "email": "string", "password": "string" }`
  - Response: `{ "message": "User created successfully" }`

- **Login**
  - `POST /api/login/`
  - Request Body: `{ "email": "string", "password": "string" }`
  - Response: `{ "message": "Login successful", "token": "string" }`

- **Logout**
  - `POST /api/logout/`
  - Request Body: `{ "token": "string" }`
  - Response: `{ "message": "Logout successful" }`

### Books

- **Add Book**
  - `POST /api/add_book/`
  - Request Body: `{ "title": "string", "author": "string", "self_rating": "number", "genre": "string", "description": "string", "cover_image": "file" }`
  - Response: `{ "message": "Book added successfully" }`

- **Search Books**
  - `GET /api/search_books/`
  - Query Parameters: `query`, `genre`, `author`, `rating`, `sort`
  - Response: `{ "items": [ ... ] }`

- **Find Books by Preference**
  - `GET /api/find_books_by_preference/`
  - Headers: `Authorization: Token <token>`
  - Response: `{ "books": [ ... ], "total_books_fetched": "number" }`

- **Get User Books**
  - `GET /api/get_user_books/`
  - Headers: `Authorization: Token <token>`
  - Response: `{ "books": [ ... ] }`

- **Get All Books**
  - `GET /api/get_all_books/`
  - Response: `{ "books": [ ... ] }`

### User Preferences

- **Update Preferences**
  - `POST /api/update_preferences/`
  - Request Body: `{ "preferences": [ "FIC", "NF", ... ] }`
  - Response: `{ "message": "Preferences updated successfully" }`

- **Get Preferences**
  - `GET /api/get_preferences/`
  - Headers: `Authorization: Token <token>`
  - Response: `{ "preferences": [ ... ] }`

## Frontend Views

- **Welcome Page**: Initial landing page.
- **Home Page**: Displays trending books, all-time favorites, and user recommendations.
- **Search Page**: Allows users to search for books with various filters.
- **Add Book Page**: Form for users to add their own books.
- **Preferences Page**: Allows users to set and update book genre preferences.

## Contributing

Feel free to open issues or submit pull requests to contribute to this project. Please ensure your contributions adhere to the project's coding standards and include appropriate tests.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or issues, please reach out to [Tanish Vashisth](mailto:tanish.vashisth@example.com).
