from django import forms
from .models import Book, Contact
from django.contrib.auth.models import User


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'


class AdminSigupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email', 'password']


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email', 'password']


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'category', 'Physical_Address']
