"""
Serializers for Big Picture Books Database.

This module contains Django Rest Framework serializers for serializing and deserializing
data related to the Big Picture Books web application. The main serializer is the
`BookSerializer` used for handling book data.

Authors:
    - Rahul Bhoyar

Classes:
    - BookSerializer: DRF serializer for serializing and deserializing book data.

Modules:
    - rest_framework.serializers: Django Rest Framework module for defining serializers.
    - .models.Book: Django model for representing books in the database.
"""

from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for handling book data.

    This serializer is used for serializing and deserializing book data when interacting
    with the Django Rest Framework API. It utilizes the `Book` model for defining the
    fields to be included in the serialized output.

    Attributes:
        - model (Book): The Django model representing books.
        - fields (str): A special string value indicating that all fields from the
          associated model should be included in the serializer.

    Example usage:
        - Serializing a book:
          ```python
          book = Book.objects.get(pk=1)
          serializer = BookSerializer(book)
          serialized_data = serializer.data
          ```
        - Deserializing data to create a new book:
          ```python
          data = {'title': 'Sample Title', 'author': 'John Doe', 'isbn': '1234567890'}
          serializer = BookSerializer(data=data)
          if serializer.is_valid():
              new_book = serializer.save()
          ```

    """
    class Meta:
        model = Book
        fields = "__all__"

