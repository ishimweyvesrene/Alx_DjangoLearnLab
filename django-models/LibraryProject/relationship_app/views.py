from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Book

# Add a new book (requires can_add_book permission)
@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        publication_year = request.POST.get('publication_year')
        isbn = request.POST.get('isbn')
        description = request.POST.get('description', '')
        
        book = Book.objects.create(
            title=title,
            author=author,
            publication_year=publication_year,
            isbn=isbn,
            description=description
        )
        return redirect('list_books')
    
    return render(request, 'relationship_app/add_book.html')


# Edit an existing book (requires can_change_book permission)
@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        book.title = request.POST.get('title')
        book.author = request.POST.get('author')
        book.publication_year = request.POST.get('publication_year')
        book.isbn = request.POST.get('isbn')
        book.description = request.POST.get('description', '')
        book.save()
        return redirect('book_detail', pk=book.pk)
    
    return render(request, 'relationship_app/edit_book.html', {'book': book})


# Delete a book (requires can_delete_book permission)
@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        book.delete()
        return redirect('list_books')
    
    return render(request, 'relationship_app/delete_book.html', {'book': book})

def is_admin(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

def is_librarian(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

def is_member(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Member'

@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html', {
        'user': request.user,
        'role': request.user.userprofile.role
    })

@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html', {
        'user': request.user,
        'role': request.user.userprofile.role
    })

@user_passes_test(is_member)
def member_view(request):
    return render(request, 'relationship_app/member_view.html', {
        'user': request.user,
        'role': request.user.userprofile.role
    })

