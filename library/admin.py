from django.contrib import admin
from .models import Book,Author,Comment,BookIssue

# Register your models here.
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display= ['author_name']

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['id' , 'book_name', 'publish_date', 'written_by']


# @admin.register(Like)
# class LikeAdmin(admin.ModelAdmin):
#     list_display = ['user' , 'book']



@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display=['user','book','text','total_likes']

@admin.register(BookIssue)
class BookIssueAdmin(admin.ModelAdmin):
    list_display = ['book', 'user','issue_date', 'return_date']