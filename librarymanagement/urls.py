"""librarymanagement URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from library import views
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [

    # Home Page Link
    path('', views.home_view, name='book_search_home'),
    path('admin/', admin.site.urls),
    path('about', views.about),
    path('allbooks', views.view_allbooks),

    # Registration Links
    path('adminsignup', views.adminsignup_view),
    path('usersignup', views.usersignup_view),
    path('adminlogin', LoginView.as_view(
        template_name='regist/adminlogin.html')),
    path('userlogin', LoginView.as_view(template_name='regist/userlogin.html')),

    # After Login Link
    path('afterlogin', views.afterlogin_view, name='book_search'),

    # Admin Links
    path('addbook', views.addbook_view),
    path('delete_book/<str:pk>/', views.delete_book, name='delete'),
    path('edit_book/<str:pk>/', views.edit_book, name='edit'),
    path('viewusers', views.view_users),
    path('contact', views.contactusers),

    # User Links
    path('borrow/<str:pk>/', views.borrow_book, name='borrow'),
    path('return/<str:pk>/', views.return_book, name='return'),
    path('borrowed', views.borrowed_books),
    path('viewbook', views.afterlogin_view),

    # Logout Link
    path('logout', LogoutView.as_view(template_name='library/index.html')),
]
