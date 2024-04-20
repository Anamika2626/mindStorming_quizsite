from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    #email = models.CharField(max_length=55, unique=True, null=True)
    bio = models.TextField(blank=True, null=True, verbose_name='Description')
    profile_img = models.ImageField(upload_to='profile_images', default='profile.png', blank=True, null=True, verbose_name='Profile image')
    location = models.CharField(max_length=100, blank=True, null=True)
    GENDER = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )
    gender = models.CharField(max_length=6, choices=GENDER, blank=True, null=True)
    
    def __str__(self):
        return self.username.username
    
    @property
    def full_name(self):
        return f"{self.username.first_name} {self.username.last_name}"