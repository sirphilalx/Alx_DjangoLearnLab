from django.db import models
from django.contrib.auth.models import User

# Assuming you have an Author model defined somewhere
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateField(auto_now_add=True)
    author = models.ForeignKey(User, related_name='blogs', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    # profile_picture = models.ImageField(upload_to='profile_pics', blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'