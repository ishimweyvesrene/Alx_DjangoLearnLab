from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # Columns to display in the list view
    list_display = ('title', 'author', 'publication_year')

    # Add a sidebar filter
    list_filter = ('publication_year', 'author')

    # Add a search box for title and author
    search_fields = ('title', 'author')
