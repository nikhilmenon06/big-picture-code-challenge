from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .description import DESCRIPTION_FOR_SWAGGER_UI 
from .views import ISBNDetailView, BookListView, index , add_book_to_library


app_name = 'app'

schema_view = get_schema_view(
    openapi.Info(
        title="Big Picture Books Database Documentation",
        default_version='v1',
        description= DESCRIPTION_FOR_SWAGGER_UI ,
        terms_of_service="#",
        contact=openapi.Contact(email="#"),
        license=openapi.License(name=""),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Frontend UI App URLs
    path('',index, name='index'),
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
