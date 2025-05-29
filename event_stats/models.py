from django.db import models

# Create your models here.

class Event(models.Model):
        
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

def __str__(self):
         return f"{self.event} - {self.country}"

