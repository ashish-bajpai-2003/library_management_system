from django.db import models
# from django.contrib.auth.models import User

# Create your models here.
class Book(models.Model):
    # user = models.OneToOneField(User, on_delete=models.CASCADE,primary_key= True)
    book_name = models.CharField(max_length= 70)
    book_cat = models.CharField(max_length= 70)
    book_publish_year= models.DateField()
