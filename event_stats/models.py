from django.db import models

# Create your models here.

class Event(models.Model):
    
    round = models.IntegerField(blank=False)
    event = models.CharField(max_length=300)
    country = models.CharField(max_length=300)
    circuit = models.CharField(max_length=300)
    city = models.CharField(max_length=300)
    date = models.CharField(max_length=300)
    first_gp = models.CharField(max_length=300)
    number_laps = models.CharField(max_length=300)
    circuit_lenght = models.CharField(max_length=300)
    race_distance = models.CharField(max_length=300)
    lap_record = models.CharField(max_length=300)
    creation_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

def __str__(self):
         return f"{self.event} - {self.country}"

