from django.contrib import admin
from .models import Book,Author,Comment,BookIssue,BorrowRecord

# Register your models here.
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display= ['author_name']

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['id' , 'book_name', 'publish_date', 'written_by','available_copies','average_rating', 'total_copies']
    search_fields = ['book_name']



@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display=['user','book','text','total_likes']

@admin.register(BookIssue)
class BookIssueAdmin(admin.ModelAdmin):
    list_display = ['book', 'user','issue_date', 'return_date']

@admin.register(BorrowRecord)
class BorrowAdmin(admin.ModelAdmin):
    list_display=['user','book','borrow_date','return_date','due_date','is_returned']