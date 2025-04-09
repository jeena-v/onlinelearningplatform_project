from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('student', 'Student'),
        ('instructor', 'Instructor'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='student')
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    
    @property
    def get_profile_picture_url(self):
        if self.profile_picture:
            return self.profile_picture.url
        else:
            return '/static/default-profile.png'  # a default image if user has no profile picture

    

    def __str__(self):
        return self.username

