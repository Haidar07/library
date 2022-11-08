from django.shortcuts import render
from django.http import HttpResponseRedirect
from . import forms
from .models import Book
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import timedelta, date
from django.core.mail import send_mail
from librarymanagement.settings import EMAIL_HOST_USER


# Home Page functions
def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    if request.method == 'POST':
        form = forms.BookForm()
        if form.is_valid:
            if request.POST.get('searchby') == 'title':
                All_Books = Book.objects.filter(
                    title=request.POST.get('search-result'))
            elif request.POST.get('searchby') == 'author':
                All_Books = Book.objects.filter(
                    author=request.POST.get('search-result'))
            else:
                All_Books = Book.objects.filter(
                    category=request.POST.get('search-result'))
            return render(request, 'library/allbooks.html', {'All_Books': All_Books})
    return render(request, 'library/index.html')


def about(request):
    return render(request, 'library/about.html')


def view_allbooks(request):
    All_Books = Book.objects.all()
    if request.method == 'POST':
        form = forms.BookForm()
        if form.is_valid:
            if request.POST.get('searchby') == 'title':
                All_Books = Book.objects.filter(
                    title=request.POST.get('search-result'))
            elif(request.POST.get('searchby' == 'author')):
                All_Books = Book.objects.filter(
                    author=request.POST.get('search-result'))
            else:
                All_Books = Book.objects.filter(
                    category=request.POST.get('search-result'))
            return render(request, 'library/allbooks.html', {'All_Books': All_Books})
    return render(request, 'library/allbooks.html', {'All_Books': All_Books})

# Registration Links

def adminsignup_view(request):
    form = forms.AdminSigupForm()
    if request.method == 'POST':
        form = forms.AdminSigupForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.set_password(user.password)
            user.save()
            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)
            return HttpResponseRedirect('adminlogin')
    return render(request, 'regist/adminsignup.html', {'form': form})


def usersignup_view(request):
    form1 = forms.UserForm()
    mydict = {'form1': form1}
    if request.method == 'POST':
        form1 = forms.UserForm(request.POST)
        if form1.is_valid():
            user = form1.save()
            user.set_password(user.password)
            user.save()
            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)
        return HttpResponseRedirect('userlogin')
    return render(request, 'regist/usersignup.html', context=mydict)


def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()


# After Login function
def afterlogin_view(request):
    if is_admin(request.user):
        All_Books = Book.objects.all()
        if request.method == 'POST':
            form = forms.BookForm()
            if form.is_valid:
                if request.POST.get('searchby') == 'title':
                    All_Books = Book.objects.filter(
                        title=request.POST.get('search-result'))
                elif(request.POST.get('searchby') == 'author'):
                    All_Books = Book.objects.filter(
                        author=request.POST.get('search-result'))
                else:
                    All_Books = Book.objects.filter(
                        category=request.POST.get('search-result'))
                return render(request, 'library/admin/adminafterlogin.html', {'All_Books': All_Books})
        return render(request, 'library/admin/adminafterlogin.html', {"All_Books": All_Books})
    else:
        All_Books = Book.objects.all()
        if request.method == 'POST':
            form = forms.BookForm()
            if form.is_valid:
                if request.POST.get('searchby') == 'title':
                    All_Books = Book.objects.filter(
                        title=request.POST.get('search-result'))
                elif(request.POST.get('searchby') == 'author'):
                    All_Books = Book.objects.filter(
                        author=request.POST.get('search-result'))
                else:
                    All_Books = Book.objects.filter(
                        category=request.POST.get('search-result'))
                return render(request, 'library/user/userafterlogin.html', {'All_Books': All_Books})
        return render(request, 'library/user/userafterlogin.html', {'All_Books': All_Books})

# Admin functions
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def addbook_view(request):
    # now it is empty book form for sending to html
    form = forms.BookForm()
    if request.method == 'POST':
        # now this form have data from html
        form = forms.BookForm(request.POST)
        if form.is_valid():
            if (Book.objects.filter(Physical_Address=form['Physical_Address'])):
                return render(request, 'library/admin/addbookfailed.html')
            form.save()
            return render(request, 'library/admin/bookadded.html')
    return render(request, 'library/admin/addbook.html', {'form': form})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def contactusers(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        data = {'full_name': full_name,
                'email': email,
                'subject': subject,
                'message': message}

        message = '''
        This email was sent From New York Library System
        
        Message Body: 
        {} 
        
        From: {}
        '''.format(data['message'], data['email'])

        send_mail(data['subject'], message, EMAIL_HOST_USER,
                  ['haidaryasine@gmail.com', data['email']])
        return render(request, 'contactus/contactsuccess.html')
    form = forms.ContactForm()
    context = {'form': form}
    return render(request, 'contactus/contact.html', context)


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_book(request, pk):
    book = Book.objects.get(id=pk)
    book.delete()
    All_Books = Book.objects.all()
    return render(request, 'library/admin/adminafterlogin.html', {'All_Books': All_Books})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def edit_book(request, pk):
    book = Book.objects.get(id=pk)
    form = forms.BookForm(instance=book)
    if request.method == 'POST':
        # now this form have data from html
        form = forms.BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return render(request, 'library/admin/bookadded.html')
    return render(request, 'library/admin/addbook.html', {'form': form})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def view_users(request):
    Books = Book.objects.all()
    L = []
    for book in Books:
        if book.status == False:
            user_id = book.Borrower_id
            user = User.objects.get(id=user_id)
            L.append([book.title, user.username, book.expiry_date])
    return render(request, 'library/admin/viewusers.html', {'L': L})

# User functions


@login_required(login_url='userlogin')
def borrow_book(request, pk):
    All_Books = Book.objects.filter(
        status=False).filter(Borrower_id=request.user.id)
    for book in All_Books:
        if (book.expiry_date <= date.today()) or (All_Books.count() > 3):
            return render(request, 'library/user/borrowsuccess.html',  {'s': False})
    book = Book.objects.get(id=pk)
    book.Borrower_id = request.user.id
    book.status = False
    book.borrow_date = date.today()
    book.expiry_date = date.today() + timedelta(days=30)
    book.save()
    return render(request, 'library/user/borrowsuccess.html', {'s': True})


@login_required(login_url='userlogin')
def return_book(request, pk):
    book = Book.objects.get(id=pk)
    book.status = True
    book.save()
    All_Books = Book.objects.filter(
        status=False).filter(Borrower_id=request.user.id)
    return render(request, 'library/user/borrowedbooks.html', {'All_Books': All_Books})


@login_required(login_url='userlogin')
def borrowed_books(request):
    All_Books = Book.objects.filter(
        status=False).filter(Borrower_id=request.user.id)
    return render(request, 'library/user/borrowedbooks.html', {'All_Books': All_Books})
