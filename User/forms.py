from django import forms
from django.core.exceptions import ValidationError
from .models import CustomUser, Books
from django.contrib.auth.hashers import make_password, check_password

class UserLoginForm(forms.Form):
    email = forms.CharField(label="Enter your email :", max_length=100)
    password = forms.CharField(label="Enter your password :", widget=forms.PasswordInput)


class UserLogoutForm(forms.Form):
    pass

class UserSignupForm(forms.Form):
    def clean(self):
        cleaned_data = super().clean()
        email_to_check = cleaned_data.get('email')
        if CustomUser.objects.filter(email=email_to_check).exists():
            raise ValidationError("Email already exists")
        
    fname = forms.CharField(label="Enter your first name :", max_length=20, required=True)
    lname = forms.CharField(label="Enter your last name :", max_length=20, required=True) 
    email = forms.EmailField(label="Enter the email :", required=True)
    password = forms.CharField(label="Enter the password :", max_length=15, widget=forms.PasswordInput)
    def clean_password(self):
        password = self.cleaned_data.get('password')
        return make_password(password)
        
GENRE_CHOICES = [
    ("Fiction", "Fiction"),
    ("Non-Fiction", "Non-Fiction"),
    ("Science Fiction", "Science Fiction"),
    ("Fantasy", "Fantasy"),
    ("Mystery", "Mystery"),
    ("Thriller", "Thriller"),
    ("Romance", "Romance"),
    ("Historical", "Historical"),
    ("Biography", "Biography"),
    ("Self-Help", "Self-Help"),
    ("Young Adult", "Young Adult"),
    ("Children's", "Children's"),
    ("Horror", "Horror"),
    ("Classic", "Classic"),
    ("Poetry", "Poetry"),
]

class BookForm(forms.Form):
    title = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'placeholder': 'Book Title'})
    )
    author = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Author'})
    )
    self_rating = forms.FloatField(
        min_value=0,
        max_value=5,
        widget=forms.NumberInput(attrs={'step': 0.1, 'placeholder': 'Rating (0-5)'})
    )
    genre = forms.ChoiceField(
        choices=GENRE_CHOICES,
        widget=forms.Select(attrs={'placeholder': 'Genre'})
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Description'})
    )
    cover_image = forms.ImageField(
        widget=forms.ClearableFileInput(attrs={'multiple': False})
    )