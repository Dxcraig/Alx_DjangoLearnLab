from django import forms
from .models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']

    def clean_title(self):
        title = self.cleaned_data.get('title', '').strip()
        if not title:
            raise forms.ValidationError('Title cannot be empty')
        return title

    def clean_publication_year(self):
        year = self.cleaned_data.get('publication_year')
        try:
            year = int(year)
        except Exception:
            raise forms.ValidationError('Publication year must be an integer')
        return year
