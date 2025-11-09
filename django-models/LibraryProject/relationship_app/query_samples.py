from relationship_app.models import Author, Book, Library, Librarian

# --- Query 1: All books by a specific author ---
def get_books_by_author(author_name):
    try:
        author = Author.objects.get(name=author_name)
        books = author.books.all()
        print(f"Books by {author.name}:")
        for book in books:
            print(f"- {book.title}")
    except Author.DoesNotExist:
        print("Author not found.")


# --- Query 2: List all books in a library ---
def get_books_in_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        books = library.books.all()
        print(f"Books in {library.name} library:")
        for book in books:
            print(f"- {book.title}")
    except Library.DoesNotExist:
        print("Library not found.")


# --- Query 3: Retrieve the librarian for a library ---
def get_librarian_for_library(library_name):
    try:
        library = Library.objects.get(name=library_name)
        librarian = library.librarian  # OneToOne relationship
        print(f"Librarian for {library.name}: {librarian.name}")
    except Library.DoesNotExist:
        print("Library not found.")
    except Librarian.DoesNotExist:
        print("No librarian assigned to this library.")


# Example usage (run in Django shell)
# python manage.py shell < relationship_app/query_samples.py
if __name__ == "__main__":
    get_books_by_author("J.K. Rowling")
    get_books_in_library("Central Library")
    get_librarian_for_library("Central Library")
