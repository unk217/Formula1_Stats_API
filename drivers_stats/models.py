from django.db import models
import datetime
from dateutil.relativedelta import relativedelta

# Create your models here.
class Drivers(models.Model):
    driver = models.CharField(max_length=300)
    driver_number = models.CharField(max_length=4)
    team = models.CharField(max_length=300)
    country = models.CharField(max_length=300)
    podiums = models.IntegerField(blank=False)
    season_points = models.FloatField(blank=False)
    total_points = models.FloatField(blank=False)
    gp_entered = models.IntegerField(blank=False)
    world_championships = models.IntegerField(blank=False)
    highest_race_finish = models.CharField(max_length=20)
    highest_grid_position = models.CharField(max_length=20)
    date_birth = models.DateField(null=True, blank=True)
    place_birth = models.CharField(max_length=100)
    creation_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def driver_age(self):
        today = datetime.date.today()
        delta = relativedelta(today, self.date_birth)
        return f"{delta.years} years"
    
    def __str__(self):
        return (self.driver)
    
    
    