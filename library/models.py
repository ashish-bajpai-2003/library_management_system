from django.db import models
from django.contrib.auth.models import User
from django.db.models import UniqueConstraint
from django.core.validators import MinValueValidator , MaxValueValidator
from datetime import date
# Create your models here.
class Author(models.Model):
    author_name = models.CharField(max_length=100)

    def __str__(self):
        return self.author_name

class Book(models.Model):
    book_name = models.CharField(max_length=100)
    authors = models.ManyToManyField(Author)
    publish_date = models.DateField()
    book_rating=models.FloatField(validators=[MinValueValidator(0),MaxValueValidator(5)],default=0.0)
    available_copies = models.IntegerField(default=1)

    def written_by(self):
        return " , ".join([str(p) for p in self.authors.all()])
    
    def __str__(self):
        return self.book_name
    
    def average_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            total_rating = sum([rating.rating for rating in ratings])
            return total_rating / len(ratings)
        return 0.0


class BookRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the user who rated
    book = models.ForeignKey(Book, on_delete=models.CASCADE)  # Link to the book being rated
    rating = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(5)])  # Rating value (0-5)
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the rating was created

    class Meta:
        unique_together = ('user', 'book')  # Ensure each user can rate the book only once

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

