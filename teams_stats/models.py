from django.db import models

# Create your models here.
class Team(models.Model):
    name=models.CharField(max_length=100)
    full_name=models.CharField(max_length=300)
    points=models.FloatField(blank=False)
    base=models.CharField(max_length=100)
    team_principal=models.CharField(max_length=100)
    chassis=models.CharField(max_length=100)
    power_unit=models.CharField(max_length=100)
    first_entry=models.CharField(max_length=100)
    world_championships=models.IntegerField(blank=False)
    highest_race_finish=models.CharField(max_length=20)
    pole_positions=models.IntegerField(blank=False)
    fastest_laps=models.IntegerField(blank=False)    
    creation_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return (self.name)