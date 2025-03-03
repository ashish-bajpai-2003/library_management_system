"""
URL configuration for library_management_system project.

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
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home,name = 'home'),
    path('signup/', views.user_signup , name ='signup'),
    path('dashboard/', views.dashboard , name ='dashboard'),
    path('user_logout/', views.user_logout , name ='user_logout'),
    path('user_login/', views.user_login , name ='user_login'),
    path('search/', views.search_books, name='search_books'),
    path('borrow/<int:book_id>/' , views.borrow_book,name = 'borrow_book'),
    path('return/<int:borrow_id>/',views.return_book,name = 'return_book'),
    path('add_book/', views.add_book, name = 'add_book'),
    path('delete_book/<int:book_id>/', views.delete_book,name= 'delete_book'),
]
