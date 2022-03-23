from django.db import models

# Create your models here.
class Movie(models.Model):
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    details = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title
