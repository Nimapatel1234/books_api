from rest_framework import serializers
from .models import Book, BookDownloadLink

class BookDownloadLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookDownloadLink
        fields = ['mime_type', 'url']


class BookSerializer(serializers.ModelSerializer):
    download_links = BookDownloadLinkSerializer(many=True, required=False)

    class Meta:
        model = Book
        fields = [
            'id', 'title', 'author_name', 'genre', 'language', 'subject',
            'bookshelf', 'download_count', 'download_links'
        ]

    def create(self, validated_data):
        download_links_data = validated_data.pop('download_links', [])
        book = Book.objects.create(**validated_data)
        for link_data in download_links_data:
            BookDownloadLink.objects.create(book=book, **link_data)
        return book
