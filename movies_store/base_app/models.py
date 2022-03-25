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
    #debt = models.FloatField()

    def get_debt(self):
        pass

    def __str__(self):
        return self.username


class RentMovie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    status = models.CharField(max_length=100)
    rent_date = models.DateField(auto_now_add=True)
    updated_date = models.DateField(auto_now=True)
    cost = models.FloatField(null=True)

    def __str__(self):
        formatted_date = self.rent_date.strftime("%-d %B %Y")
        return f"{self.user.username} rented {self.movie.title} on {formatted_date}"

    def get_cost(self):
        time_passed = self.updated_date - self.rent_date
        days_passed = time_passed.days
        if days_passed <= 3:
            self.cost = days_passed
        else:
            self.cost = 3 + (days_passed-3) * 0.5
        return self.cost
