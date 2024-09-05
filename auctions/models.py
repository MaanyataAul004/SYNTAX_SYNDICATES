from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Disaster_report(models.Model):
    Disaster_choices = [
        ('flood', 'Flood'),
        ('road_block', 'Road Blockage'),
        ('damage', 'Damage'),
        ('earthquake', 'Earthquake'),
        ('wildfire', 'Wildfire'),
        ('tornado','Tornado'),
        ('hurricane','Hurricane'),
        ('industrial_accident','Industrial Accident'),
        ('landslide','Landslide'),
        ('other','Other')
    ]
    disaster_type = models.CharField(max_length=50, choices=Disaster_choices)
    location = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='report_images/', blank=True, null=True)
    reported_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.disaster_type} at {self.location}"