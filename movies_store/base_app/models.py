from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import date

# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    details = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title

class User(AbstractUser):
    movies_rented = models.ManyToManyField(Movie, through="RentMovie")

    def get_debt(self):
        pass

    def __str__(self):
        return self.username


class RentMovie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    status = models.CharField(max_length=100)
    rent_date = models.DateField(default=date.today)
    updated_date = models.DateField(default=date.today)
    cost = models.FloatField(null=True)

    def __str__(self):
        formatted_date = self.rent_date.strftime("%-d %B %Y")
        return f"{self.user.username} rented {self.movie.title} on {formatted_date}"
