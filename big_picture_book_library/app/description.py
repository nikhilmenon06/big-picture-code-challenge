DESCRIPTION_FOR_SWAGGER_UI = """
# Big Picture Books Database API

**Overview:**
Users can enter the ISBN number of a book. Our application will fetch the book's details from an external API and save it to our database. 




**Endpoints:**

1. **Fetch Book Details by ISBN**
    - `GET /isbn/<isbn>`: Returns a JSON including: author, title, summary, cover_url.

2. **Save Book Details to our Library**
    - `POST /books` with body JSON: `{isbn: "ISBN_NUMBER_HERE"}`: This will save the book's details to our library database.

3. **List All Books in our Library**
    - `GET /books`: Returns a list of all books stored in our library. Use a format, so the frontend can render all information from this one JSON.


**Usage Instructions:**

- Ensure to use valid ISBN numbers when making requests.

"""
