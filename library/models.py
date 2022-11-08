from django.db import models
from django.contrib.auth.models import User
from datetime import date, datetime, timedelta


class User(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    def Integer(self):
        return self.user.id


def get_expiry():
    return datetime.today() + timedelta(days=30)


class Book(models.Model):
    catchoice = [
        ('education', 'Education'),
        ('entertainment', 'Entertainment'),
        ('comics', 'Comics'),
        ('biography', 'Biography'),
        ('history', 'History'),
        ('novel', 'Novel'),
        ('fantasy', 'Fantasy'),
        ('thriller', 'Thriller'),
        ('romance', 'Romance'),
        ('scifi', 'Sci-Fi'),
        ('science', 'Science')
    ]
    title = models.CharField(max_length=30)
    author = models.CharField(max_length=40)
    category = models.CharField(
        max_length=30, choices=catchoice, default=None)
    Physical_Address = models.CharField(max_length=40)
    status = models.BooleanField(default=True)
    borrow_date = models.DateField(default=date.today())
    expiry_date = models.DateField(default=get_expiry())
    Borrower_id = models.IntegerField(max_length=20, null=True, default=None)
#    slug = models.SlugField(max_length=100)
#   cover_image = models.ImageField(upload_to = 'img', blank = True, null = True)

    def __str__(self):
        return self.title

    def toString(self):
        return self.Borrower_id.username


class BookSearch(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.name_of_book


class Contact(models.Model):
    full_name = models.CharField(max_length=30, default="")
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self):
        return self.email
