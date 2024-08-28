from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.contrib.auth import get_user_model

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.IntegerField()

    def __str__(self):
        return f"{self.title} by {self.author}"
    

# custom authentication methods
# todo:
# 1. Override the email authentication
# 2. Override the password authentication
# 3. Create a User manager
# 4. Register the User model with django admin
class User(AbstractUser):
    email = models.EmailField(unique=True, max_length=255)
    username = models.CharField(unique=False, max_length=255)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email