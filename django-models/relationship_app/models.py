from django.db import models

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} by {self.author}"
    

class Library(models.Model):
    name = models.CharField(max_length=200)
    books = models.ManyToManyField(Book, related_name="books")

    def __str__(self):
        return f"the name of the library where {self.books} is, is {self.name}"
    


class Librarian(models.Model):
    name = models.CharField(max_length=200)
    library = models.ManyToManyField(Library, related_name="libraries")
