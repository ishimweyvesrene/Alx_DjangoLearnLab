# bookshelf/forms.py
from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "author", "publication_year"]

    def clean_title(self):
        title = self.cleaned_data.get("title", "")
        # Example sanitization - strip whitespace; additional checks allowed
        return title.strip()

class SearchForm(forms.Form):
    q = forms.CharField(max_length=200, required=False)

    def clean_q(self):
        q = self.cleaned_data.get("q", "")
        return q.strip()
