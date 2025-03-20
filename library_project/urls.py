"""
URL configuration for library_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from library import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home , name = 'home'),
    path('search/', views.search_books, name='search_books'),
    path('login/' , views.login, name = 'user_login'),
    path('signup/', views.signup, name = 'user_signup'),
    path('dashboard/',views.dashboard, name = 'dashboard'),
    path('book_detail/<int:pk>/', views.book_detail, name = 'book_detail'),
    # path('like/<int:pk>/', views.like_book,name = 'like_book'),
    path('comments/<int:id>/',views.addcomment,name='comment'),
    path('like/<int:id>/',views.book_like, name='like-book'),
    path('logout/' , views.logout , name = 'user_logout'),
    path('rate/<int:book_id>/',views.rate_book, name='rate_book'),
    path('deletecomment/<int:id>/' , views.deletecomment, name = 'delcomment'),
    path('issue_book/<int:book_id>/' , views.issue_book, name = 'issue_book'),
    path('books/', views.book_list,name='book_list'),
    path('book/return/<int:book_id>/', views.return_book, name='return_book'),
    path('borrow/<int:book_id>/',views.borrow_book, name='borrow_book'),
    path('return/<int:borrow_id>/', views.return_book, name='return_book'),
    path('logout/', views.user_logout, name='user_logout'), 
]
