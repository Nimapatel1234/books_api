from django.urls import path
from .views import register_user, login_user, logout_user,book_list_page, books_page, BookListView, BookDetailView

urlpatterns = [
    path('', register_user, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('books/', books_page, name='books-page'),
    path('api/books/', BookListView.as_view(), name='book-list'),
    path('api/books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
     path('data/', book_list_page, name='data-page'),
]

