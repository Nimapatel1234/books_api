from django.shortcuts import render, get_object_or_404 ,redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from .models import Book
from .serializers import BookSerializer
from rest_framework.pagination import PageNumberPagination
# from .utils import list_books
from .models import Book
from rest_framework.permissions import IsAdminUser , IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import IntegrityError


from django.db import connection
# Register User (Admin Only)
def register_user(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        messages.error(request, "Only admin users can register new accounts.")
        return redirect('login')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if not username or not email or not password:
            messages.error(request, "All fields are required.")
            return redirect('register')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('register')

        try:
            User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, 'Registration successful.')
            return redirect('login')
        except IntegrityError as e:
            messages.error(request, f"Database error: {e}")
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {e}")

    return render(request, 'register.html')

# Login User
def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful')
            return redirect('books-page')  # Redirect to books page
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'login.html')

# Logout User
def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('login')


def list_books():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM books LIMIT 10;")
        results = cursor.fetchall()
        for row in results:
            print(row)


# HTML rendering for books page

# Books Page
def books_page(request):
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to view this page.")
        return redirect('login')
    return render(request, "books.html")
# Custom pagination class
class CustomPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 100

class BookRawQueryView(APIView):
    def get(self, request):
        books = Book.objects.all()[:10]  # Fetch first 10 books
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)




def book_list_page(request):
    books = Book.objects.all()  # Retrieve all books from the database
    return render(request, "data.html", {"books": books})

# API View for book list and creation
class BookListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        books =books = Book.objects.all()
        paginator = CustomPagination()
        paginated_books = paginator.paginate_queryset(books, request)
        serializer = BookSerializer(paginated_books, many=True)
        return paginator.get_paginated_response(serializer.data)
 

    def post(self, request):
        # Create a new book
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# API View for detailed book operations
class BookDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        # Retrieve a single book by ID
        book = get_object_or_404(Book, pk=pk)
        serializer = BookSerializer(book)
        return Response(serializer.data)

    def put(self, request, pk):
        # Update a book by ID
        book = get_object_or_404(Book, pk=pk)
        serializer = BookSerializer(book, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        # Delete a book by ID
        book = get_object_or_404(Book, pk=pk)
        book.delete()
        return Response({"message": "Book deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
