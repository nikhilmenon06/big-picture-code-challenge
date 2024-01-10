"""
Tests for Big Picture Books Database.

This module contains Django tests for the Big Picture Books web application. It includes
tests for models, views, and other functionalities.

Authors:
    - Rahul Bhoyar

Modules:
    - django.test: Django module for running tests.
    - django.urls.reverse: Django module for reversing URL patterns.
    - .models.Book: Django model for representing books in the database.
    - .views.ISBNDetailView: View class for handling ISBN details.
    - .views.BookListView: View class for handling book list.
"""

from django.test import TestCase
from django.urls import reverse
from .models import Book

class BookModelTest(TestCase):
    """
    Test case for the Book model.

    This test case includes tests for creating a new book instance and checking its
    string representation.

    Methods:
        - test_book_creation: Test creating a new book instance.
        - test_book_str_representation: Test the string representation of a book.

    """
    def test_book_creation(self):
        """Test creating a new book instance."""
        book = Book.objects.create(
            title='Sample Title',
            author='John Doe',
            isbn='1234567890123',
            publisher='Publisher ABC',
            cover_page_url='https://example.com/cover.jpg',
            language='English'
        )
        self.assertEqual(book.title, 'Sample Title')
        self.assertEqual(book.author, 'John Doe')
        self.assertEqual(book.isbn, '1234567890123')
        self.assertEqual(book.publisher, 'Publisher ABC')
        self.assertEqual(book.cover_page_url, 'https://example.com/cover.jpg')
        self.assertEqual(book.language, 'English')

    def test_book_str_representation(self):
        """Test the string representation of a book."""
        book = Book.objects.create(title='Sample Title', author='John Doe', isbn='1234567890123')
        self.assertEqual(str(book), 'Sample Title')


class ISBNDetailViewTest(TestCase):
    """
    Test case for the ISBNDetailView.

    This test case includes tests for fetching book details by ISBN.

    Methods:
        - test_valid_isbn_detail: Test fetching details for a valid ISBN.
        - test_invalid_isbn_detail: Test fetching details for an invalid ISBN.

    """
    def test_valid_isbn_detail(self):
        """Test fetching details for a valid ISBN."""
        book = Book.objects.create(title='Little Women', author='Louisa May Alcott', isbn='9782743433956')
        response = self.client.get(reverse('app:isbn_detail', args=['9782743433956']))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['title'], 'Little Women')


    def test_invalid_isbn_detail(self):
        """Test fetching details for an invalid ISBN."""
        response = self.client.get(reverse('app:isbn_detail', args=['invalid_isbn']))
        self.assertEqual(response.status_code, 400)


class BookListViewTest(TestCase):
    """
    Test case for the BookListView.

    This test case includes tests for fetching the list of all books.

    Methods:
        - test_book_list_view: Test fetching the list of all books.

    """
    def test_book_list_view(self):
        """Test fetching the list of all books."""
        Book.objects.create(title='Book 1', author='Author 1', isbn='1234567890111')
        Book.objects.create(title='Book 2', author='Author 2', isbn='1234567890222')
        response = self.client.get(reverse('app:book_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['title'], 'Book 1')
        self.assertEqual(response.data[1]['title'], 'Book 2')
