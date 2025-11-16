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


class ExampleForm(forms.Form):
    """Small example form used in documentation/tests demonstrating
    safe input handling and validation.
    """
    name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)

    def clean_name(self):
        value = self.cleaned_data.get('name', '').strip()
        if not value:
            raise forms.ValidationError('Name is required')
        return value

    def clean_message(self):
        msg = self.cleaned_data.get('message', '')
        # Very small example of sanitization: trim and limit length
        msg = msg.strip()
        if len(msg) > 2000:
            raise forms.ValidationError('Message too long')
        return msg
