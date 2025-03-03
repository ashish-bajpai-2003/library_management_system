from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta




class Author(models.Model):
    author_name=models.CharField(max_length=70)

    def __str__(self):
        print(self.author_name)
        return self.author_name

class Book(models.Model):
    book_name=models.CharField(max_length=50)
    book_publish_year=models.DateField()
    authors=models.ManyToManyField(Author)
    is_borrowed = models.BooleanField(default=False)

    def  written_by(self):
        return " , ".join([str(p) for p in self.authors.all()])
    


class Borrow(models.Model):
    book = models.ForeignKey(Book,on_delete= models.CASCADE)
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    borrow_date = models.DateTimeField(default=timezone.now)
    due_date = models.DateTimeField(null = True,blank = True)
    returned_date = models.DateTimeField(null = True,blank = True)
    late_fee = models.DecimalField(max_digits=5, decimal_places=2,default=0.00)
   
    def save(self, *args, **kwargs):
       # Ensure `due_date` is calculated only if it's not already set
        if not self.due_date:
            self.due_date = self.borrow_date + timedelta(days=7) 
        super(Borrow, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} borrowed {self.book.book_name}"
    


    def calculate_late_fee(self):
        if self.is_overdue():
            overdue_days = (timezone.now() - self.due_date).days
            self.late_fee = overdue_days * 5
            self.save()


    def __str__(self):
        return f"{self.book.book_name} borrowed by {self.user.username}"