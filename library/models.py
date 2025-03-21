from django.db import models
from django.contrib.auth.models import User
from django.db.models import UniqueConstraint
from django.core.validators import MinValueValidator , MaxValueValidator
from datetime import date
from datetime import timedelta

# Create your models here.
class Author(models.Model):
    author_name = models.CharField(max_length=100)

    def __str__(self):
        return self.author_name

class Book(models.Model):
    book_name = models.CharField(max_length=100)
    authors = models.ManyToManyField(Author)
    publish_date = models.DateField(null=True, blank=True)
    book_rating = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5)], default=0.0)
    available_copies = models.IntegerField(default=1)
    book_sr_no = models.CharField(max_length=10, unique=True)
    total_copies = models.PositiveBigIntegerField(default=1)
    status = models.CharField(max_length=10, default='available')

    def written_by(self):
        return " , ".join([str(p) for p in self.authors.all()])

    def __str__(self):
        return self.book_name
    

    def average_rating(self):
        ratings = self.ratings.all()  # This will now work because of related_name='ratings'
        if ratings.exists():
            total_rating = sum(rating.rating for rating in ratings)
            return total_rating / ratings.count()  
        return 0.0


class BookRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the user who rated
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='ratings')  # Link to the book being rated with related_name='ratings'
    rating = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5)])  # Rating value (0-5)
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the rating was created

    class Meta:
        constraints = [
            UniqueConstraint(fields=['user', 'book'], name='unique_user_book_rating')  # Ensure each user can rate the book only once
        ]

    def __str__(self):
        return f"Rating by {self.user.username} for {self.book.book_name}"
    

   
    
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    text = models.TextField()
    likes = models.ManyToManyField(User,related_name='comment_likes', blank=True)


    
    def total_likes(self):
        return self.likes.count()



class BookIssue(models.Model):
    book = models.ForeignKey(Book , on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    issue_date = models.DateField(default=date.today)
    return_date= models.DateField(null=True,blank= True)
    is_returned=models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} - {self.book.book_name}'



class BorrowRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateField(auto_now_add=True)
    return_date = models.DateField(null=True, blank=True)
    due_date = models.DateField(default=date.today() + timedelta(days=14))
    is_returned = models.BooleanField(default=False)
    def _str_(self):
        return f"{self.user.username} borrowed {self.book.book_name}"
    def book_sr_no(self):
        return self.book.book_sr_no