from django import forms
from django.core.exceptions import ValidationError
# from api.models import User
from .models import CustomUser
from django.contrib.auth.hashers import make_password, check_password

class UserLoginForm(forms.Form):
    email = forms.CharField(label="Enter your email :", max_length=100)
    password = forms.CharField(label="Enter your password :", widget=forms.PasswordInput)


class UserLogoutForm(forms.Form):
    pass

class UserSignupForm(forms.Form):
    def clean(self):
        cleaned_data = super().clean()
        email_to_check = clean_data.get('email')
        if CustomUser.objects.filter(email=email_to_check).exists():
            raise ValidationError("Email already exists")
        
    fname = forms.CharField(label="Enter your first name :", max_length=20, required=True)
    lname = forms.CharField(label="Enter your last name :", max_length=20, required=True) 
    email = forms.EmailField(label="Enter the email :", required=True)
    password = forms.CharField(label="Enter the password :", max_length=15, widget=forms.PasswordInput)
    def clean_password(self):
        password = self.cleaned_data.get('password')
        return make_password(password)

# class addBookForm(forms.Form):
