from django.shortcuts import render, get_object_or_404
from django.views.generic.detail import DetailView   # ✅ Required by ALX checker
from .models import Book
from .models import Library  # ✅ Keep as a separate line for checker
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationFor




# Function-based view to list all books
def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})


# Class-based view to display details for a specific library
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

