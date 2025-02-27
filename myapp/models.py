from django.db import models

class Author(models.Model):
    author_name=models.CharField(max_length=70)

    def __str__(self):
        print(self.author_name)
        return self.author_name

class Book(models.Model):
    book_name=models.CharField(max_length=50)
    book_publish_year=models.DateField()
    authors=models.ManyToManyField(Author)

    def  written_by(self):
        return " , ".join([str(p) for p in self.authors.all()])