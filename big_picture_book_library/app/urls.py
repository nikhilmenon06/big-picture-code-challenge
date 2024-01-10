"""
URL Configuration for Big Picture Books Database.

This module defines the URL patterns for the Big Picture Books Django web application.
It includes both frontend UI app URLs, backend API endpoints, and Swagger/Redoc UI URLs
for documentation purposes.

Authors:
    - Rahul Bhoyar
    
URL Patterns:
    - Frontend UI App URLs:
        - '' (index): Main page displaying a list of books and an ISBN search form.
        - 'success': Page for adding a book to the library with ISBN search results.

    - Backend API Endpoints URLs:
        - 'isbn/<isbn>/': Endpoint for retrieving details of a book by ISBN.
        - 'books/': Endpoint for retrieving the list of all books.

    - Swagger UI URLs:
        - 'swagger/<str:format>': URL for accessing the Swagger JSON representation.
        - 'swagger/': URL for accessing the Swagger UI for API documentation.

    - Redoc UI URLs:
        - 'redoc/': URL for accessing the ReDoc UI for API documentation.

Modules:
    - django.urls: Django module for defining URL patterns.
    - rest_framework.permissions: Django Rest Framework module for defining permissions.
    - drf_yasg.views.get_schema_view: DRF Yasg module for generating API schema.
    - drf_yasg.openapi: DRF Yasg module for defining OpenAPI specifications.
    - .description: Module containing the description for Swagger UI.
    - .views.ISBNDetailView: View class for handling ISBN details.
    - .views.BookListView: View class for handling book list.
    - .views.index: View function for rendering the main page.
    - .views.add_book_to_library: View function for adding a book to the library.

Constants:
    - app_name: Name of the Django app.
    - schema_view: DRF Yasg schema view with API information.
    - urlpatterns: List of URL patterns for the Django app.

"""
from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .description import DESCRIPTION_FOR_SWAGGER_UI 
from .views import ISBNDetailView, BookListView, index, add_book_to_library


app_name = 'app'

schema_view = get_schema_view(
    openapi.Info(
        title="Big Picture Books Database Documentation",
        default_version='v1',
        description=DESCRIPTION_FOR_SWAGGER_UI,
        terms_of_service="#",
        contact=openapi.Contact(email="#"),
        license=openapi.License(name=""),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Frontend UI App URLs
    path('', index, name='index'),
    path('success', add_book_to_library, name='add_book_to_library'), 
    
    # Backend API Endpoints URLs
    path('isbn/<isbn>/', ISBNDetailView.as_view(), name='isbn_detail'),
    path('books/', BookListView.as_view(), name='book_list'),  
    
    # Swagger UI URLs
    path('swagger/<str:format>', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    
    # Redoc UI URLs
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
