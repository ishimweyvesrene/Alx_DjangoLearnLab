from rest_framework import serializers
from .models import Author, Book
import datetime


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for Book model.
    Includes custom validation to prevent adding a book with
    a publication year in the future.
    """

    class Meta:
        model = Book
        fields = '__all__'

    # Custom validation
    def validate_publication_year(self, value):
        current_year = datetime.datetime.now().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for Author model.
    Includes nested BookSerializer to show books belonging to this author.
    """
    books = BookSerializer(many=True, read_only=True)  # Nested serializer

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']

def perform_create(self, serializer):
    serializer.save()  # You can add logging or user assignment

def get_queryset(self):
    qs = Book.objects.all()
    year = self.request.query_params.get('year')
    if year:
        qs = qs.filter(publication_year=year)
    return qs
