from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200, default='Unknown')
    author = models.CharField(max_length=100, default='Unknown')
    publication_year = models.IntegerField(default=1900)

    def __str__(self):
        return f"{self.title} by {self.author}"