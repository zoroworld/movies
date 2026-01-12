from django.utils import timezone

from django.db import models
from cities_light.models import Country, Region, City


# Create your models here.
class Location(models.Model):
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)
    state = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    address = models.CharField(max_length=50, default='')

    def __str__(self):
        parts = [p for p in [
            self.city.name if self.city else None,
            self.state.name if self.state else None,
            self.country.name if self.country else None,
        ] if p]
        return ", ".join(parts)




class Seat(models.Model):
    seat = models.IntegerField(default=0)
    price = models.IntegerField(default=40)
    is_available = models.BooleanField(default=True)

    class seat_types(models.TextChoices):
        VIP = 'VIP'
        NORMAL = 'NORMAL'

    type = models.CharField(max_length=20, choices=seat_types.choices, default='NORMAL')

    def __str__(self):
        return f"{self.seat}"


class Schedule(models.Model):
    movie = models.ForeignKey('movies.Movie', on_delete=models.CASCADE)
    start_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)

    class schedule_types(models.TextChoices):
        HOURLY = 'HOURLY'
        DAILY = 'DAILY'
        WEEKLY = 'WEEKLY'
        MONTHLY = 'MONTHLY'

    type = models.CharField(max_length=20, choices=schedule_types.choices, default='HOURLY')

    def __str__(self):
        return self.movie.title


class Theatre(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(null=True, blank=True)
    movies = models.ManyToManyField('movies.Movie', related_name='theatres')
    schedules = models.ManyToManyField(Schedule,  blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True, blank=True)
    seats = models.ManyToManyField(Seat)

    def __str__(self):
        return self.name


class TimeSlot(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.start_time} - {self.end_time}"



class Show(models.Model):
    movie = models.ForeignKey('movies.Movie', on_delete=models.CASCADE, related_name='shows')
    theatre = models.ForeignKey('Theatre', on_delete=models.CASCADE, related_name='shows')
    date = models.DateField(default=timezone.now)
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.CASCADE,  null=True, blank=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"📅 {self.movie.title} at {self.start_time}"

class ShowSeat(models.Model):
    show = models.ForeignKey(Show, related_name="show_seats", on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, related_name="seat_shows", on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)


