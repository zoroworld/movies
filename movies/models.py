from cities_light.models import Country, Region, City

from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()

    class Genre(models.TextChoices):
        Drama = 'Drama'
        Fantasy = 'Fantasy'
        Action = 'Action'
        Horror = 'Horror'
        Adventure = 'Adventure'
        Comedy = 'Comedy'
        Music = 'Music'
        Romance = 'Romance'
        SciFi = 'SciFi'
        Thriller = 'Thriller'



    genre = models.CharField(max_length=20, choices=Genre.choices)
    poster = models.ImageField(upload_to='posters/', default='posters/default.jpg')
    date = models.DateField(null=True)
    release_date = models.DateField(default=None)

    def __str__(self):
        return self.title


