DESCRIPTION_FOR_SWAGGER_UI = """
# Big Picture Books Database API
### Contributors : Rahul Bhoyar ###
### Last updated on : 10/01/2024 ###

## Overview
The Big Picture Books Database API provides a seamless interface for users to interact with our comprehensive book management system. Users can enter the ISBN number of a book, and our application orchestrates a two-step process:

1. **Fetch External Data:**
   - Utilizing the provided ISBN, the system queries an external API to retrieve enriched information about the book, including author, title, summary, cover URL, and other relevant details.

2. **Store Locally:**
   - The fetched data is then stored securely in our local database, creating a robust library of books with accurate and up-to-date information.

## Key Features:

- **Dynamic Data Enrichment:**
  - Leverages external APIs to ensure the latest and most comprehensive details for each book.

- **User-Friendly Interaction:**
  - Simplifies user experience by requiring only the ISBN number to access a wealth of information about a book.

- **Centralized Book Database:**
  - Creates a centralized repository of book data, facilitating easy retrieval and management.

- **Error Handling:**
  - Implements detailed error handling to provide users and developers with clear feedback in case of invalid requests or server issues.

- **Interactive Documentation:**
  - Explore and test the API interactively using the provided Swagger UI documentation.

## Endpoints

### 1. Fetch Book Details by ISBN
- **Method**: GET
- **Endpoint**: `/isbn/<isbn>`
- **Description**: Returns detailed information about a book based on its ISBN number, including author, title, summary, and cover URL.
- **Parameters**:
  - `isbn` (path): The ISBN number of the book to fetch.

### 2. Save Book Details to our Library
- **Method**: POST
- **Endpoint**: `/books`
- **Body**: JSON: `{"isbn": "ISBN_NUMBER_HERE"}`
- **Description**: Saves the book's details to our library database. The provided ISBN number is used to fetch data from an external API and store it locally.
- **Request Body**:
  - `isbn` (string): The ISBN number of the book to save.

### 3. List All Books in our Library
- **Method**: GET
- **Endpoint**: `/books`
- **Description**: Returns a list of all books stored in our library. The response is formatted to allow easy rendering on the frontend.
- **Response**:
  - List of books with details such as author, title, summary, and cover URL.

## Usage Instructions

- Ensure you use valid ISBN numbers when making requests.

## Important Notes

- The API leverages external data sources to enrich our book database with accurate and up-to-date information.
- Detailed error handling is implemented to provide informative responses in case of invalid requests or server errors.

---

"""
