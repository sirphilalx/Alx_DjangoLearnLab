from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.contrib.auth import get_user_model

from django.contrib.auth.models import BaseUserManager

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
    
    class Meta:
        permissions = [
            ('can_add_book', 'Can add book'),
            ('can_change_book', 'Can change book'),
            ('can_delete_book', 'Can delete book'),
        ]
    

class Library(models.Model):
    name = models.CharField(max_length=200)
    books = models.ManyToManyField(Book, related_name="books")

    def __str__(self):
        return f"the name of the library where {self.books} is, is {self.name}"
    


class Librarian(models.Model):
    name = models.CharField(max_length=200)
    library = models.ManyToManyField(Library, related_name="libraries")


# user profile models 


# Extending User Model Using a One-To-One Link
class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Librarian', 'Librarian'),
        ('Member', 'Member'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.role}"
    




# base user manager

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

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

    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email