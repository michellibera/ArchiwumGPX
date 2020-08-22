from django.contrib.gis.db import models
from django.contrib import admin
from django.contrib.gis import admin as geoadmin
from django.db.models.manager import Manager
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse




class gpxfile(models.Model):
    title = models.CharField("Title", max_length=100)
    description = models.CharField("Description", max_length=200)
    callsign = models.CharField("Callsign", max_length=100)
    date = models.DateTimeField(default=timezone.now)
    gpx_file = models.FileField(upload_to='gpxstorage/')

    def __str__(self):
        return self.title



class gpxtrack(models.Model):
    title = models.CharField("Nazwa", max_length=100)
    description = models.CharField("Opis", max_length=200)
    date = models.DateTimeField("Data",default=timezone.now)
    gpx_file = models.FileField("Plik GPX",upload_to='gpxstorage/')
    author = models.ForeignKey(User, on_delete=models.CASCADE,)

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        self.gpx_file.delete()
        super().delete(*args, **kwargs)    

    def get_absolute_url(self):
        return reverse('gpxtrack-detail', kwargs={'pk': self.pk})




class gpxcompare(models.Model):
    title = models.CharField("Nazwa", max_length=100)
    description = models.CharField("Opis", max_length=200)
    date = models.DateTimeField("Data",default=timezone.now)
    gpx_file_track = models.FileField("Pierwszy Plik",upload_to='gpxstorage/')
    gpx_file_route = models.FileField("Drugi Plik",upload_to='gpxstorage/')
    author = models.ForeignKey(User, on_delete=models.CASCADE,)

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        self.gpx_file_track.delete()
        self.gpx_file_route.delete()
        super().delete(*args, **kwargs)  

    def get_absolute_url(self):
        return reverse('compare-detail', kwargs={'pk': self.pk})

