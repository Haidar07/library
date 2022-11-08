from django.contrib import admin
from .models import Book, User
# Register your models here.


class BookAdmin(admin.ModelAdmin):
    pass

admin.site.register(Book, BookAdmin)


class StudentExtraAdmin(admin.ModelAdmin):
    pass


admin.site.register(User, StudentExtraAdmin)
