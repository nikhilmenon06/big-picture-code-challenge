"""
Views for Big Picture Books Database.

This module contains Django views for handling various functionalities in the Big
Picture Books web application. Views include fetching book details, managing the book
list, rendering the main page, and adding books to the library.

Authors:
    - Rahul Bhoyar
    
Classes:
    - ISBNDetailView: API view for fetching book details by ISBN number.
    - BookListView: API view for managing the list of books in the library database.

Functions:
    - index: View function for rendering the main page.
    - add_book_to_library: View function for adding a book to the library.

Modules:
    - django.shortcuts: Django module for shortcuts, like rendering templates.
    - django.http: Django module for HTTP-related functionalities.
    - rest_framework.status: Django Rest Framework module for HTTP status codes.
    - rest_framework.response.Response: DRF module for creating HTTP responses.
    - rest_framework.views.APIView: DRF module for creating class-based views.
    - drf_yasg.utils.swagger_auto_schema: DRF Yasg module for automatic schema generation.
    - drf_yasg.openapi: DRF Yasg module for defining OpenAPI specifications.
    - .models.Book: Django model for representing books in the database.
    - .serializers.BookSerializer: DRF serializer for serializing book data.

Constants:
    - EXPECTED_RESPONSES: Dictionary mapping HTTP status codes to OpenAPI responses.
"""


import re
import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseServerError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Book
from .serializers import BookSerializer


EXPECTED_RESPONSES = {
    200: openapi.Response('OK', BookSerializer()),
    201: openapi.Response('Created', BookSerializer()),
    204: openapi.Response('No Content'),
    400: openapi.Response('Bad Request', BookSerializer()),
    401: openapi.Response('Unauthorized'),
    403: openapi.Response('Forbidden'),
    404: openapi.Response('Not Found'),
    405: openapi.Response('Method Not Allowed'),
    500: openapi.Response('internal_server_error. Need to be checked from back end.'),
}


def validate_isbn(isbn):
    """
    Validates an ISBN (International Standard Book Number).

    Parameters:
    - isbn (str or int): The input ISBN to be validated. It can be a string or an integer.

    Returns:
    - bool: True if the ISBN is valid (either ISBN-10 or ISBN-13), False otherwise.

    This function takes an ISBN as input and validates it by removing hyphens and spaces,
    then determining whether it is a valid ISBN-10 or ISBN-13. If the ISBN is valid, the
    function returns True; otherwise, it returns False.
    """
    isbn = str(isbn)
    # Remove hyphens and spaces from the ISBN
    cleaned_isbn = re.sub(r'[-\s]', '', isbn)
    # Check if the ISBN is either ISBN-10 or ISBN-13
    if len(cleaned_isbn) == 10:
        return validate_isbn10(cleaned_isbn)
    elif len(cleaned_isbn) == 13:
        return validate_isbn13(cleaned_isbn)
    else:
        return False


def validate_isbn10(isbn):
    if not re.match(r'^\d{9}[\dXx]$', isbn):
        return False
    # Calculate the checksum for ISBN-10
    checksum = sum(int(digit) * (i + 1) for i, digit in enumerate(isbn[:-1]))
    checksum %= 11
    checksum = 'X' if checksum == 10 else str(checksum)
    return checksum == isbn[-1].upper()


def validate_isbn13(isbn):
    if not re.match(r'^\d{13}$', isbn):
        return False
    # Calculate the checksum for ISBN-13
    checksum = sum(int(digit) * (1 if i % 2 == 0 else 3) for i, digit in enumerate(isbn[:-1]))
    checksum %= 10
    checksum = (10 - checksum) % 10

    return checksum == int(isbn[-1])


def cover_image_url(isbn_number):
    """
    Generates the URL for the cover image of a book based on its ISBN number.

    Parameters:
    - isbn_number (str or int): The ISBN number of the book.

    Returns:
    - str: The URL of the cover image for the specified ISBN number.

    This function takes an ISBN number as input and constructs the URL for the cover
    image using the Open Library Covers API. The generated URL points to the large-sized
    cover image (suffix -L.jpg). The function returns the complete URL as a string.
    """
    url = f"https://covers.openlibrary.org/b/isbn/{isbn_number}-L.jpg"
    return url


def validate_response(response, isbn, api_url):
    """
    Validates the response from the Open Library API and extracts book information.

    Parameters:
    - response (requests.Response): The response object from the Open Library API.
    - isbn (str or int): The ISBN number used in the API request.
    - api_url (str): The URL of the Open Library API used for the request.

    Returns:
    - dict or dict-like: If the response is valid, it returns a dictionary containing
      information about the first book in the response. If there are errors in the
      response, it returns a dictionary describing the encountered issues.

    This function checks the validity of the response from the Open Library API based on
    the HTTP status code and the structure of the JSON data. It ensures that the response
    contains the expected 'docs' object, a list of books, and extracts information from
    the first book in the list if it meets the expected structure. If any issues are
    encountered, an error dictionary is returned with details about the problem.
    """
    if response.status_code != 200:
        # Handle HTTP error responses
        return {
            'error': 'Error from server side.',
            'error_explanation': 'There is no data available for this request from Open Library APIs server.',
            'level_of_error': 1,
            'status_code': response.status_code,
            'issue_with_isbn': isbn,
            'api_url': api_url
        }

    response_data = response.json()

    if not isinstance(response_data, dict):
        # Handle unexpected JSON format
        return {
            'error': 'Error from server side.',
            'error_explanation': 'There is no data available for this request from Open Library APIs server.',
            'error_details': 'We did not receive expected output for this request.',
            'level_of_error': 2,
            'issue_with_isbn': isbn,
            'api_url': api_url
        }

    docs_object = response_data.get('docs')

    if docs_object is None:
        # Handle missing 'docs' object
        return {
            'error': 'Error from server side.',
            'error_explanation': 'There is no data available for this request from Open Library APIs server.',
            'error_details': 'There is no \'docs\' object in response.',
            'level_of_error': 3,
            'issue_with_isbn': isbn,
            'api_url': api_url
        }

    if not isinstance(docs_object, list):
        # Handle unexpected type for 'docs' object
        return {
            'error': 'Error from server side.',
            'error_explanation': 'There is no data available for this request from Open Library APIs server.',
            'error_details': 'The type of \'docs\' object is not a list.',
            'level_of_error': 4,
            'issue_with_isbn': isbn,
            'api_url': api_url
        }

    if len(docs_object) < 1:
        # Handle empty 'docs' object
        return {
            'error': 'Error from server side.',
            'error_explanation': 'There is no data available for this request from Open Library APIs server.',
            'error_details': 'The list in \'docs\' object does not have a minimum of 1 book data. There is no data available for this ISBN number.',
            'level_of_error': 5,
            'issue_with_isbn': isbn,
            'api_url': api_url
        }

    first_book = docs_object[0]

    if not isinstance(first_book, dict):
        # Handle unexpected type for objects in the list
        return {
            'error': 'Error from server side.',
            'error_explanation': 'There is no data available for this request from Open Library APIs server.',
            'error_details': 'The type of object in the list is not a dictionary. Hence, we cannot parse the data.',
            'level_of_error': 6,
            'issue_with_isbn': isbn,
            'api_url': api_url
        }

    keys_expected = ["title", "author_name", "publisher", "language"]

    for key in keys_expected:
        # Check for missing or empty values in the expected keys
        if key not in first_book or not first_book[key]:
            return {
                'error': 'Error from server side.',
                'error_explanation': 'There is no data available for this request from Open Library APIs server.',
                'error_details': f"The key '{key}' is either not present or has an empty value.",
                'level_of_error': 7,
                'issue_with_isbn': isbn,
                'api_url': api_url
            }

    # If everything is valid, return the information about the first book
    return first_book


def isbn_invalidation_error_response(isbn, type_of_request):
    """
    Generates an error response for invalid ISBN in client-side requests.

    Parameters:
    - isbn (str or int): The invalid ISBN provided in the request.
    - type_of_request (str): The type of request (e.g., 'cover_image', 'book_info').

    Returns:
    - dict: A dictionary containing details of the client-side ISBN validation error.

    This function creates an error response for client-side requests with an invalid ISBN.
    The response includes information about the error, explanation, and details, along with
    the provided ISBN, the type of request, and the error level.
    """
    error_data = {
        'error': 'Error from client side.',
        'error_explanation': 'There is no data available for this request from Open Library APIs server.',
        'error_details': 'The ISBN is incorrect. Please provide the correct ISBN.',
        'level_of_error': 0,
        'issue_with_isbn': isbn,
        'type_of_request': type_of_request
    }
    return error_data


def fetch_book_data(isbn):
    """
    Fetches book data from the Open Library API based on the provided ISBN.

    Parameters:
    - isbn (str or int): The ISBN number of the book.

    Returns:
    - dict or dict-like: A dictionary containing information about the book, including
      title, author, ISBN, cover page URL, language, and publisher. If there are errors
      in the API response or ISBN validation, an error dictionary is returned.

    This function initiates a request to the Open Library API using the provided ISBN
    and validates the response using the `validate_response` function. If the response
    is valid, it extracts relevant information about the first book, including title,
    author, ISBN, cover page URL, language, and publisher. If there are errors in the
    response or ISBN validation, the function returns an error dictionary with details
    about the issue.
    """
    api_url = f"https://openlibrary.org/search.json?isbn={isbn}"
    response = requests.get(api_url)
    first_book = validate_response(response, isbn, api_url)

    if "error" in first_book.keys():
        return first_book

    title = first_book.get('title', 'Title not available')
    author_name = first_book.get('author_name', ['Author not available'])[0]
    publisher = first_book.get('publisher', ['Publisher not available'])[0]
    language = first_book.get('language', ['Language not available'])[0]
    cover_image = cover_image_url(isbn)

    updated_book_data = {
        'title': title,
        'author': author_name,
        'isbn': isbn,
        'cover_page_url': cover_image,
        'language': language,
        'publisher': publisher
    }
    return updated_book_data

       
class ISBNDetailView(APIView):
    """
    API view for fetching book details by ISBN number.

    This view provides an endpoint to retrieve book details, including author, title, ISBN,
    and cover page URL, for a given ISBN number.

    Parameters:
    - isbn (str): The ISBN number of the book.

    Responses:
    - 200 OK: Successful response with serialized book details.
    - 400 Bad Request: If the provided ISBN is invalid.
    - 500 Internal Server Error: If there are internal server errors during the request.

    Example usage:
    GET /api/book-details/{isbn}/

    Swagger Documentation:
    - operation_summary: Fetch Book Details by ISBN number.
    - operation_description: Returns book details like author, title, ISBN, and cover page URL for a given ISBN.
    - parameters:
        - name: isbn
          required: true
          in: path
          description: ISBN number
    """

    @swagger_auto_schema(
        operation_summary="Fetch Book Details by ISBN number.",
        operation_description="Returns book details like author, title, ISBN, and cover page URL for a given ISBN. Note that ISBN should not contain any special characters.",
        responses=EXPECTED_RESPONSES,
        parameters=[{"name": "isbn", "required": True, "in": "path", "description": "ISBN number"}],
    )
    def get(self, request, isbn):
        """
        Handles GET requests for fetching book details by ISBN.

        If the provided ISBN is invalid, a 400 Bad Request response is returned with
        details about the validation error. If there are internal server errors during
        the request, a 500 Internal Server Error response is returned with details about
        the encountered error. Otherwise, a 200 OK response is returned with serialized
        book details.

        Parameters:
        - isbn (str): The ISBN number of the book.

        Returns:
        - Response: The HTTP response containing book details or error information.
        """
        if not validate_isbn(isbn):
            error_data = isbn_invalidation_error_response(isbn, "get")
            return Response(error_data, status=status.HTTP_400_BAD_REQUEST)

        updated_book_data = fetch_book_data(isbn)

        if "error" in updated_book_data:
            updated_book_data["type_of_request"] = "get"
            updated_book_data["type_of_error"] = 'internal_server_error'
            return Response(updated_book_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = BookSerializer(data=updated_book_data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data)

        
class BookListView(APIView):
    """
    API view for managing the list of books in the library database.

    This view provides endpoints to fetch the list of all books and save book details
    to the library database.

    Responses:
    - 200 OK: Successful response with serialized list of books.
    - 201 Created: Successful response when a new book is added to the database.
    - 400 Bad Request: If the provided ISBN in the request is invalid.
    - 500 Internal Server Error: If there are internal server errors during the request.

    Example usage:
    GET /api/books/
    POST /api/books/

    Swagger Documentation:
    - get:
        operation_summary: Fetch the list of all books from the library database.
        operation_description: Returns book details like author, title, ISBN, and cover page URL for a book.
        parameters:
          - name: isbn
            required: true
            in: path
            description: ISBN number
    - post:
        operation_summary: Save Book Details to our library database.
        operation_description: Saves the book's details to our library database. Please provide the valid ISBN number
        in the request. It should be either a 10-digit or 13-digit ISBN Number.
        parameters:
          - name: isbn
            required: true
            in: path
            description: ISBN number
        request_body:
          required: true
          content:
            application/json:
              schema:
                type: object
                properties:
                  isbn:
                    type: string
                required:
                  - isbn
        responses: EXPECTED_RESPONSES
    """

    @swagger_auto_schema(
        operation_summary="Fetch the list of all books from the library database.",
        operation_description="Returns book details like author, title, ISBN, and cover page URL for a book.",
        parameters=[{"name": "isbn", "required": True, "in": "path", "description": "ISBN number"}],
        responses=EXPECTED_RESPONSES
    )
    def get(self, request):
        """
        Handles GET requests to fetch the list of all books in the library database.

        Returns:
        - Response: The HTTP response containing the serialized list of books.
        """
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Save Book Details to our library database.",
        operation_description="Saves the book's details to our library database. Please provide the valid ISBN number in the request. It should be either a 10-digit or 13-digit ISBN Number. Note that ISBN should not contain any special characters.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'isbn': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['isbn'],
        ),
        responses=EXPECTED_RESPONSES
    )
    def post(self, request):
        """
        Handles POST requests to save book details to the library database.

        If the provided ISBN is invalid, a 400 Bad Request response is returned with
        details about the validation error. If there are internal server errors during
        the request, a 500 Internal Server Error response is returned with details about
        the encountered error. Otherwise, a 201 Created response is returned when the
        book details are successfully added to the database.

        Returns:
        - Response: The HTTP response containing information about the added book or an error.
        """
        isbn = request.data.get('isbn')
        if not validate_isbn(isbn):
            error_data = isbn_invalidation_error_response(isbn, "post")
            return Response(error_data, status=status.HTTP_400_BAD_REQUEST)

        updated_book_data = fetch_book_data(isbn)

        if "error" in updated_book_data:
            return Response({'internal_server_error': updated_book_data, 'type_of_request': 'post'},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        serializer = BookSerializer(data=updated_book_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response_body = {
            "status": "201 OK",
            "book_added_to_databases": True,
            "title": updated_book_data["title"],
            "isbn": updated_book_data["isbn"],
        }

        return Response(response_body, status=status.HTTP_201_CREATED)


def index(request):
    """
    View function for the main index page.

    This view fetches the list of all books from the library database and displays them
    in descending order by primary key (latest first). It also allows users to search
    for book details by ISBN using a POST request.

    Parameters:
    - request (HttpRequest): The HTTP request object.

    Returns:
    - HttpResponse: The HTTP response containing the rendered HTML page.
    """
    books = Book.objects.all().order_by('-pk')
    context = {'books': books}

    if request.method == 'POST':
        isbn_number = request.POST.get('search_query')
        if validate_isbn(isbn_number):
            response = fetch_book_data(isbn_number)
            request.session['context'] = response
            return render(request, 'app/book_details.html', request.session['context'])

    return render(request, 'app/index.html', context)


def add_book_to_library(request):
    """
    View function for adding a book to the library.

    This view handles the submission of a book using a POST request. It validates the
    ISBN number, fetches book details, and saves the book to the library database.

    Parameters:
    - request (HttpRequest): The HTTP request object.

    Returns:
    - HttpResponse: The HTTP response containing the rendered HTML page.
    """
    if request.method == 'POST':
        context = request.session.get('context', {})
        isbn_number = context.get('isbn')

        if not validate_isbn(isbn_number):
            error_data = isbn_invalidation_error_response(isbn_number, "post")
            return HttpResponseServerError(error_data, status=status.HTTP_400_BAD_REQUEST)

        updated_book_data = fetch_book_data(isbn_number)
        serializer = BookSerializer(data=updated_book_data)
        
        if serializer.is_valid():
            serializer.save()
            request.session['context'] = serializer.data
            return render(request, 'app/success.html', request.session['context'])
        else:
            return HttpResponseServerError({'error': 'Failed to save book to the library.'},
                                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    request.session.pop('context', None)
    return render(request, 'app/success.html', context)


