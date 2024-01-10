"""
Admin Configuration for Big Picture Books Database.

This module contains the Django admin configuration for the Big Picture Books web
application. It includes the registration of the `Book` model to make it manageable
through the Django admin interface.

Authors:
    - Rahul Bhoyar

Modules:
    - django.contrib.admin: Django module for configuring the admin interface.
    - .models.Book: Django model for representing books in the database.
"""

from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Book model.

    This class configures the display of the Book model in the Django admin interface.
    It provides options for customizing how the book data is presented and managed.

    Attributes:
        - list_display (list): A list of model fields to be displayed in the admin list view.
        - search_fields (list): A list of model fields to be searchable in the admin interface.
        - list_filter (list): A list of model fields for creating filters in the admin interface.

    Example usage:
        - Registering the Book model in admin.py:
          ```python
          @admin.register(Book)
          class BookAdmin(admin.ModelAdmin):
              list_display = ('title', 'author', 'isbn', 'publisher')
              search_fields = ('title', 'author', 'isbn', 'publisher')
              list_filter = ('language',)
          ```
    """
    list_display = ('title', 'author', 'isbn', 'publisher')
    search_fields = ('title', 'author', 'isbn', 'publisher')
    list_filter = ('language',)
