
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from . import views
from django.urls import path, include
from django.urls import path
from .views import RegisterView, ProfileView, ProfileUpdateView
from django.contrib.auth import views as auth_views


urlpatterns = [
    # Authentication URLs
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('register/', views.register, name='register'),
    
    # Role-based access URLs
    path('admin/', views.admin_view, name='admin_view'),
    path('librarian/', views.librarian_view, name='librarian_view'),
    path('member/', views.member_view, name='member_view'),
    
    path('admin/', admin.site.urls),
    path('', include('relationship_app.urls')),
    path('books/', views.list_books, name='list_books'),
    path('books/<int:pk>/', views.book_detail, name='book_detail'),
    path('books/add/', views.add_book, name='add_book'),
    path('books/<int:pk>/edit/', views.edit_book, name='edit_book'),
    path('books/<int:pk>/delete/', views.delete_book, name='delete_book'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='accounts:login'), name='logout'),
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
    path('profile/edit/', ProfileUpdateView.as_view(), name='profile_edit'),
    
]


