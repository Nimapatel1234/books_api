# from django.urls import path
# from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
# from .views import BookListView, books_page, BookDetailView ,BookRawQueryView ,book_list_page

# urlpatterns = [
#     path('api/books/raw/', BookRawQueryView.as_view(), name='book-raw-query'),
#     path('data/', book_list_page, name='data-page'),

#     path('api/books/', BookListView.as_view(), name='book-list'),
#     path('api/books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
#     path('books/', books_page, name='books-page'),
#     path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
#     path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
# ]

from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from .views import BookListView, BookDetailView, books_page, book_list_page

urlpatterns = [
    path('api/books/', BookListView.as_view(), name='book-list'),
    path('api/books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('books/', books_page, name='books-page'),
    path('data/', book_list_page, name='data-page'),
]

