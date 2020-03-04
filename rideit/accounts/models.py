from django.db import models

from django.contrib.auth.models import User

class UserProfile(models.Model):
    """Model that builds on Django's User Model."""

    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)

    first_name = models.CharField(default="", max_length=32, help_text='First name')
    last_name = models.CharField(default="", max_length=32, help_text='Last name')
    email = models.EmailField(default="", max_length=64, help_text='Enter a valid email address')
    number = models.CharField(default="", max_length=10, help_text="Mobile Phone Number")

    profile_pic = models.ImageField(upload_to="profile_pics", max_length=500, default="", null=True)
