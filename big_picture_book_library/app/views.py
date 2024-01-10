import re
import requests
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
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
    url = f"https://covers.openlibrary.org/b/isbn/{isbn_number}-L.jpg"
    return url 

def validate_response(response, isbn, api_url):
    if response.status_code != 200:
        return {
            'error': 'Error from server side.',
            'error_explanation': 'There is no data available for this request from Open Library APIs server.',
            'level_of_error': 1,
            'status_code': response.status_code,
            'issue_with_isbn': isbn,
            'api_url':api_url
        }
    response_data = response.json()
    if not isinstance(response_data, dict):
        return {
            'error': 'Error from server side.',
            'error_explanation': 'There is no data available for this request from Open Library APIs server.',
            'error_details': 'We did not receive expected output for this request.',
            'level_of_error': 2,
            'issue_with_isbn': isbn,
            'api_url':api_url
        }
    docs_object = response_data.get('docs')
    if docs_object is None:
        return {
            'error': 'Error from server side.',
            'error_explanation': 'There is no data available for this request from Open Library APIs server.',
            'error_details': 'There is no \'docs\' object in response.',
            'level_of_error': 3,
            'issue_with_isbn': isbn,
            'api_url':api_url
        }
    if not isinstance(docs_object, list):
        return {
            'error': 'Error from server side.',
            'error_explanation': 'There is no data available for this request from Open Library APIs server.',
            'error_details': 'The type of \'docs\' object is not a list.',
            'level_of_error': 4,
            'issue_with_isbn': isbn,
            'api_url':api_url
        }  
    if len(docs_object) < 1:
        return {
            'error': 'Error from server side.',
            'error_explanation': 'There is no data available for this request from Open Library APIs server.',
            'error_details': 'The list in \'docs\' object does not have a minimum of 1 book data. There is no data availabe for this ISBN number.',
            'level_of_error': 5,
            'issue_with_isbn': isbn,
            'api_url':api_url
        }
    first_book = docs_object[0]
    if not isinstance(first_book, dict):
        return {
            'error': 'Error from server side.',
            'error_explanation': 'There is no data available for this request from Open Library APIs server.',
            'error_details': 'The type of object in the list is not a dictionary. Hence, we cannot parse the data.',
            'level_of_error': 6,
            'issue_with_isbn': isbn,
            'api_url':api_url
        }
    keys_expected = ["title", "author_name", "publisher", "language"]
    for key in keys_expected:
        if key not in first_book or not first_book[key]:
            return {
                'error': 'Error from server side.',
                'error_explanation': 'There is no data available for this request from Open Library APIs server.',
                'error_details': f"The key '{key}' is either not present or has an empty value.",
                'level_of_error': 7,
                'issue_with_isbn': isbn,
                'api_url':api_url
            }
    return first_book

def isbn_invalidation_error_response(isbn, type_of_request):
    error_data = {
        'error': 'Error from client side.',
        'error_explanation': 'There is no data available for this request from Open Library APIs server.',
        'error_details': 'The ISBN is incorrect. Please provide the correct ISBN.',
        'level_of_error': 0,
        'issue_with_isbn': isbn,
        'type_of_request' :type_of_request}
    return error_data

def fetch_book_data(isbn):
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
    @swagger_auto_schema(
    operation_summary="Fetch Book Details by ISBN number.",
    operation_description="Returns book details like author, title, ISBN, and cover page URL for a given ISBN.",
    responses=EXPECTED_RESPONSES,
    parameters=[{"name": "isbn", "required": True, "in": "path", "description": "ISBN number"}],)
       
    def get(self, request, isbn):
        if not validate_isbn(isbn):
            error_data = isbn_invalidation_error_response(isbn, "get")
            return Response(error_data, status=status.HTTP_400_BAD_REQUEST)
        updated_book_data = fetch_book_data(isbn)
        if "error" in updated_book_data:
            updated_book_data["type_of_request"] = "get"
            updated_book_data["type_of_error"] = 'internal_server_error'
            return Response(updated_book_data,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        serializer = BookSerializer(data=updated_book_data)
        serializer.is_valid(raise_exception=True)    
        return Response(serializer.data)
        
class BookListView(APIView):
    @swagger_auto_schema(
        operation_summary="Fetch the list of all books from the library database.",
        operation_description="Returns book details like author, title, ISBN, and cover page URL for a book.",
        parameters=[{"name": "isbn", "required": True, "in": "path", "description": "ISBN number"}],
        responses=EXPECTED_RESPONSES
    )
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        operation_summary="Save Book Details to our library database.",
        operation_description="Saves the book's details to our library database. Please provide the valid ISBN number in the request.It should be either 10-digit or 13 digit ISBN Number.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'isbn': openapi.Schema(type=openapi.TYPE_STRING),},
            required=['isbn'],
        ),
        responses=EXPECTED_RESPONSES
    )
           
    def post(self, request):
        isbn = request.data.get('isbn') 
        if not validate_isbn(isbn):
            error_data = isbn_invalidation_error_response(isbn, "post")
            return Response(error_data, status=status.HTTP_400_BAD_REQUEST)
        updated_book_data = fetch_book_data(isbn)
        if "error" in updated_book_data:
            return Response({'internal_server_error': updated_book_data, 'type_of_request':'post'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        serializer = BookSerializer(data=updated_book_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response_body = {
            "status": "201 OK",
            "book_added_to_databases": True,
            "title":updated_book_data["title"],
            "isbn":updated_book_data["isbn"],
        }
        return Response(response_body, status=status.HTTP_201_CREATED)

def index(request):
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
    if request.method == 'POST':
        context = request.session.get('context', {})
        isbn_number = context.get('isbn')
        if not validate_isbn(isbn_number):
            error_data = isbn_invalidation_error_response(isbn_number, "post")
            return Response(error_data, status=status.HTTP_400_BAD_REQUEST)
        updated_book_data = fetch_book_data(isbn_number)
        serializer = BookSerializer(data=updated_book_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        request.session['context'] = serializer.data
        return render(request, 'app/success.html', request.session['context'])
    request.session.pop('context', None)
    return render(request, 'app/success.html', context)


