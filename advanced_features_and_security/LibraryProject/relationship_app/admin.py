from django.contrib import admin
from .models import UserProfile
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    list_filter = ('role',)
    search_fields = ('user__username',)

# Register your models here.
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year', 'isbn')
    search_fields = ('title', 'author', 'isbn')
    list_filter = ('publication_year',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    list_filter = ('role',)

class CustomUserAdmin(UserAdmin):
    model = CustomUser

    # Add date_of_birth and profile_photo to admin display & forms
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('date_of_birth', 'profile_photo')}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('date_of_birth', 'profile_photo')}),
    )

    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'date_of_birth')
    ordering = ('username',)