from django.contrib import admin
from django.urls import path, include
from library import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home , name = 'home'),
    path('search/', views.search_books, name='search_books'),
    path('login/' , views.login, name = 'user_login'),
    path('signup/', views.signup, name = 'user_signup'),
    path('dashboard/',views.dashboard, name = 'dashboard'),
    path('book_detail/<int:pk>/', views.book_detail, name = 'book_detail'),
    path('comments/<int:id>/',views.addcomment,name='comment'),
    path('like/<int:id>/',views.book_like, name='like-book'),
    path('rate/<int:book_id>/',views.rate_book, name='rate_book'),
    path('deletecomment/<int:id>/' , views.deletecomment, name = 'delcomment'),
    path('issue_book/<int:book_id>/' , views.issue_book, name = 'issue_book'),
    path('books/', views.book_list,name='book_list'),
    path('book/return/<int:book_id>/', views.return_book, name='return_book'),
    path('borrow/<int:book_id>/',views.borrow_book, name='borrow_book'),
    path('return/<int:borrow_id>/', views.return_book, name='return_book'),
    path('logout/', views.userlogout, name='userlogout'), 
    path('my-borrowed-books/', views.my_borrowed_books, name='my_borrowed_books'),

    path('oauth/', include('social_django.urls', namespace='social')),
    # path('oauth/', include('social_django.urls', namespace='social')),
]
