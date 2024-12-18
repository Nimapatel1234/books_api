from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import register_user, login_user, logout_user, books_page, BookListView, BookDetailView, book_list_page , BookRawQueryView

schema_view = get_schema_view(
    openapi.Info(
        title="Books API",
        default_version='v1',
        description="API documentation for managing books",
        contact=openapi.Contact(email="nima2001patel@gmail.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', register_user, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('books/', books_page, name='books-page'),
    path('data/', book_list_page, name='data-page'),
    path('api/books/', BookListView.as_view(), name='book-list'),
    path('api/books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('books/raw/', BookRawQueryView.as_view(), name='book-raw-query'), 
    # Swagger URLs
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
