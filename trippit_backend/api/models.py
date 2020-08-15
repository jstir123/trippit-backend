from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True)
    profilePicURL = models.TextField(null=True, blank=True)

class Trip(models.Model):
    user = models.ForeignKey(User, related_name='trips', blank=False, on_delete=models.CASCADE)
    location = models.CharField(max_length=150, blank=False)
    city = models.CharField(max_length=60, null=True, blank=True)
    state = models.CharField(max_length=60, null=True, blank=True)
    country = models.CharField(max_length=60, null=True, blank=True)
    lat = models.FloatField(blank=False)
    lon = models.FloatField(blank=False)
    description = models.TextField(null=True, blank=True)
    startDate = models.DateField(null=True, blank=True)
    endDate = models.DateField(null=True, blank=True)
    loggedAt = models.DateField(auto_now_add=True)

class TripPicture(models.Model):
    trip = models.ForeignKey(Trip, related_name='pictures', blank=False, on_delete=models.CASCADE)
    name = models.CharField(max_length=60, blank=False)
    url = models.TextField(blank=False)

class TripItinerary(models.Model):
    trip = models.ForeignKey(Trip, related_name='itinerary', blank=False, on_delete=models.CASCADE)
    place = models.CharField(max_length=60, blank=False)
    category = models.CharField(max_length=15, blank=False)
    isRecommended = models.BooleanField(blank=False)