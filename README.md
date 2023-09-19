# Big Picture Coding Challenge - Backend - Book Library API

Our colleagues have amassed an impressive collection of books, leading to quite the bill and an unhappy boss. To keep things organized and to provide transparency into our library, we've decided to step in and help with software. Our solution: a sleek website where our intern can easily record books by their ISBN number, pulling in detailed information via an API.

**Your mission**: Build the backend to power this application.

## Overview:

- Users (in this case, our intern) can enter the ISBN number of a book.
- Our software will fetch the book's details from an external API and save it to our database.
- The frontend will then display our entire library in a user-friendly manner.

## Backend Specifications:

### Technology:

- Python (Any backend framework of your choice. E.g., Flask, Django, FastAPI, etc.)
- Database: Feel free to choose what you're comfortable with (SQLite, PostgreSQL, MongoDB, etc.)

### Features:

1. **ISBN Validation**:
    - The backend should be able to validate an ISBN number.
    - If the ISBN is not valid, it should send an appropriate response to the frontend.

2. **Fetch Book Details**:
    - The backend should get book details like author, title, summary, and cover URL from a third-party API.
    - Hint: Check out [OpenLibrary's API](https://openlibrary.org/). It's free and provides detailed information on books by ISBN.

3. **Endpoints**:

    - **Task 1**: Fetch Book Details by ISBN

      `GET /isbn/<isbn>`:
      - Returns a JSON including: author, title, summary, cover_url.

    - **Task 2**: Save Book Details to our Library

      `POST /books` with body `JSON: {isbn: "ISBN_NUMBER_HERE"}`:
      - This will save the book's details to our library database.

    - **Task 3**: List All Books in our Library

      `GET /books`:
      - Returns a list of all books stored in our library.
      - Use a format, so the fronend can render all information from this one JSON

## Documentation:

Please ensure that you document your code adequately. Proper commenting will not only help you in future modifications but will also assist any other developer who might be working with your code.

Please create a new branch for your code. Do not add anything to the Master branch.

Good luck, and may your code run without bugs!
