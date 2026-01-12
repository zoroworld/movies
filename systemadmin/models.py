from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class NewUser(AbstractUser):
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50)
    contact = models.CharField(max_length=20, blank=True)
    is_admin = models.BooleanField(default=False)
    profile_pic = models.ImageField(upload_to='profile_pics', default='profile_pics/default.pg')
