from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    details = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title

class User(AbstractUser):
    movies_rented = models.ManyToManyField(Movie)
    debt = models.FloatField()

    def get_debt(self):
        pass

    def __str__(self):
        return self.username
