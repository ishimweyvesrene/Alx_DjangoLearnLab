# Django Admin Integration for Book Model

## Step 1: Import and Register Book Model
File: bookshelf/admin.py
```python
from django.contrib import admin
from .models import Book
admin.site.register(Book)
