from django.db import models
from django.utils import timezone


class Movie(models.Model):
    title = models.CharField(max_length=50, blank=True)
    year = models.IntegerField(blank=True)
    plot = models.CharField(max_length=500, blank=True)
    language = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=8, blank=True)


class Comment(models.Model):
    text = models.CharField(max_length=50, blank=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
