from rest_framework import generics, filters as drf_filters
from django_filters import rest_framework as filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Book
from .serializers import BookSerializer



"""
BOOK LIST VIEW
- Provides read-only access to all books
- Anyone (authenticated or not) can view the list
"""
class BookListView(generics.ListAPIView):
    """
    Book List API View

    Features Added:
    - Filtering by title, author, publication_year
    - Searching by book title and author name
    - Ordering results by title or publication_year

    Usage Examples:
    - /api/books/?title=Atomic%20Habits
    - /api/books/?search=Chimamanda
    - /api/books/?ordering=-publication_year
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]

    # Enable filtering, searching and ordering
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]

    # Filtering fields
    filterset_fields = ['title', 'author', 'publication_year']

    # Searching fields (text search)
    search_fields = ['title', 'author__name']

    # Ordering fields
    ordering_fields = ['title', 'publication_year']

    # Default ordering
    ordering = ['title']


"""
BOOK DETAIL VIEW
- Retrieves a single book by ID
- Anyone can view (read-only)
"""
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]  # Public access


"""
BOOK CREATE VIEW
- Creates a new Book instance
- Only authenticated users can create books
- Validates publication year via BookSerializer
"""
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]  # Auth required

    # Optional: Customize create behavior (example: auto log)
    def perform_create(self, serializer):
        # Custom behavior can be added here (like logging)
        serializer.save()


"""
BOOK UPDATE VIEW
- Updates an existing book record
- Only authenticated users can update
- DRF automatically handles validation & partial updates
"""
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Custom validation or additional logic can be added
    def perform_update(self, serializer):
        serializer.save()


"""
BOOK DELETE VIEW
- Deletes a book
- Only authenticated users are allowed to delete
"""
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
