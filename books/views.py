from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from .models import Book
from .serializers import BookSerializer
from rest_framework.pagination import PageNumberPagination
# from .utils import list_books
from .models import Book


from django.db import connection

def list_books():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM books LIMIT 10;")
        results = cursor.fetchall()
        for row in results:
            print(row)


# HTML rendering for books page
def books_page(request):
    return render(request, "books.html")


# Custom pagination class
class CustomPagination(PageNumberPagination):
    page_size = 25
    page_size_query_param = 'page_size'
    max_page_size = 100

class BookRawQueryView(APIView):
    def get(self, request):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM books LIMIT 10;")
            results = cursor.fetchall()
            return Response(results)


def book_list_page(request):
    books = Book.objects.all()  # Retrieve all books from the database
    return render(request, "data.html", {"books": books})

# API View for book list and creation
class BookListView(APIView):
    def get(self, request):
        books = Book.objects.all()[:25]  # Fetch top 25 books
        return Response({"books": list(books.values())})
    # def get(self, request):
    #     # Retrieve all books with filters and pagination
    #     filters = Q()
    #     if 'language' in request.GET:
    #         filters &= Q(language__in=request.GET['language'].split(','))
    #     if 'topic' in request.GET:
    #         filters &= Q(subject__icontains=request.GET['topic']) | Q(bookshelf__icontains=request.GET['topic'])
    #     if 'author_name' in request.GET:
    #         filters &= Q(author_name__icontains=request.GET['author_name'])
    #     if 'title' in request.GET:
    #         filters &= Q(title__icontains=request.GET['title'])

    #     books = Book.objects.filter(filters).order_by('-download_count')
    #     paginator = CustomPagination()
    #     paginated_books = paginator.paginate_queryset(books, request)
    #     serializer = BookSerializer(paginated_books, many=True)
    #     return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        # Create a new book
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# API View for detailed book operations
class BookDetailView(APIView):
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
