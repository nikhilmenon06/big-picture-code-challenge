"""
Models for Big Picture Books Database.

This module contains Django models for representing data related to the Big Picture Books
web application. The main model defined in this file is the `Book` model.

Authors:
    - Rahul Bhoyar

Classes:
    - Book: Django model for representing book data.

Modules:
    - django.db.models: Django module for defining database models.
"""

from django.db import models

class Book(models.Model):
    """
    Django model for representing book data.

    This model defines the structure of the 'Book' database table, including fields
    such as title, author, ISBN, publisher, cover page URL, and language.

    Attributes:
        - title (CharField): The title of the book.
        - author (CharField): The author of the book.
        - isbn (CharField): The ISBN (International Standard Book Number) of the book.
        - publisher (CharField): The publisher of the book.
        - cover_page_url (URLField, optional): The URL to the cover page image of the book.
        - language (CharField, optional): The language in which the book is written.

    Methods:
        - __str__: Returns a string representation of the book, used for display purposes.

    Example usage:
        - Creating a new book instance:
          ```python
          new_book = Book.objects.create(
              title='Sample Title',
              author='John Doe',
              isbn='1234567890123',
              publisher='Publisher ABC',
              cover_page_url='https://example.com/cover.jpg',
              language='English'
          )
          ```
        - Querying books from the database:
          ```python
          books = Book.objects.all()
          for book in books:
              print(book.title)
          ```

    """
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13)
    publisher = models.CharField(max_length=255)  
    cover_page_url = models.URLField(blank=True, null=True)  
    language = models.CharField(max_length=50, blank=True, null=True) 
    
    def __str__(self):
        return self.title


