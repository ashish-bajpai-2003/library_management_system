from django.contrib import admin
from .models import Book,Author , Borrow
# Register your models here.

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display=['id','author_name']

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display=['id','book_name','book_publish_year','written_by']

@admin.register(Borrow)
class BorrowAdmin(admin.ModelAdmin):
    list_display = ['book' , 'user' , 'borrow_date' , 'due_date', 'returned_date', 'late_fee']