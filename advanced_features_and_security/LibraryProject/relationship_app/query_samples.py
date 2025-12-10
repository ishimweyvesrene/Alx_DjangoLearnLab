from relationship_app.models import Author, Book, Library, Librarian

# Query all books by a specific author
def get_books_by_author(author_name):
    try:
        author = Author.objects.get(name=author_name)
        books = Book.objects.filter(author=author)
        print(f"Books by {author.name}:")
        for book in books:
            print(book.title)
    except Author.DoesNotExist:
        print("Author not found.")


# List all books in a library
def get_books_in_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()
        print(f"Books in {library.name}:")
        for book in books:
            print(book.title)
    except Library.DoesNotExist:
        print("Library not found.")


# Retrieve the librarian for a library
def get_librarian_for_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        librarian = Librarian.objects.get(library=library)
        print(f"Librarian for {library.name}: {librarian.name}")
    except Library.DoesNotExist:
        print("Library not found.")
    except Librarian.DoesNotExist:
        print("No librarian assigned to this library.")
