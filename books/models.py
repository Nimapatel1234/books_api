from django.db import models

# Create your models here.


class Author(models.Model):
    name = models.CharField(max_length=255)

class Book(models.Model):
    title = models.CharField(max_length=255)
    author_name = models.CharField(max_length=255)  # Store author name directly
    genre = models.CharField(max_length=100, null=True, blank=True)
    language = models.CharField(max_length=50)
    subject = models.TextField(null=True, blank=True)
    bookshelf = models.TextField(null=True, blank=True)
    download_count = models.IntegerField(default=0)

class BookDownloadLink(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="download_links")
    mime_type = models.CharField(max_length=50)
    url = models.URLField()

