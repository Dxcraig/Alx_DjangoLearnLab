from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post


class CustomUserCreationForm(UserCreationForm):
    """
    Extended user registration form that includes email field.
    
    Inherits from Django's UserCreationForm and adds:
    - Email field (required)
    - Custom validation for email uniqueness
    """
    email = forms.EmailField(
        required=True,
        help_text='Required. Enter a valid email address.',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})
    
    def clean_email(self):
        """
        Validate that the email is unique.
        """
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email address is already registered.')
        return email
    
    def save(self, commit=True):
        """
        Save the user with the email field.
        """
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    """
    Form for updating user profile information.
    
    Allows users to update:
    - Username
    - Email
    - First name
    - Last name
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def clean_email(self):
        """
        Validate that the email is unique (excluding current user).
        """
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('This email address is already in use.')
        return email


class PostForm(forms.ModelForm):
    """
    Form for creating and updating blog posts.
    
    Fields:
    - title: Post title (max 200 characters)
    - content: Post content (TextField)
    
    The author field is automatically set in the view and not included in the form.
    """
    title = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter post title'
        }),
        help_text='Maximum 200 characters'
    )
    
    content = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 10,
            'placeholder': 'Write your post content here...'
        }),
        help_text='Write your blog post content'
    )
    
    class Meta:
        model = Post
        fields = ['title', 'content']
    
    def clean_title(self):
        """
        Validate that the title is not empty or just whitespace.
        """
        title = self.cleaned_data.get('title')
        if not title or not title.strip():
            raise forms.ValidationError('Title cannot be empty.')
        return title.strip()
    
    def clean_content(self):
        """
        Validate that the content is not empty or just whitespace.
        """
        content = self.cleaned_data.get('content')
        if not content or not content.strip():
            raise forms.ValidationError('Content cannot be empty.')
        return content.strip()
