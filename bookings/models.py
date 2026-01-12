from django.utils import timezone
from django.db import models

# Create your models here.

class Booking(models.Model):
    movies = models.ForeignKey('movies.Movie', on_delete=models.CASCADE)
    seats = models.ManyToManyField("theatres.Seat")
    user = models.ForeignKey('systemadmin.NewUser', on_delete=models.CASCADE)
    book_date = models.DateTimeField(default=timezone.now)
    total_price = models.IntegerField(default=0)
    paid = models.BooleanField(default=False)
    theater = models.CharField(max_length=100, default='')
    address = models.TextField(max_length=255, default='')
    show = models.ForeignKey('theatres.Show', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.movies.title