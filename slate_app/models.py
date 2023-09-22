from django.db import models


# Create your models here.
class Slate(models.Model):
    #We are going to follow the same logic as DK does as far as feature names, etc
    position = models.CharField(max_length=20)
    name_id = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    player_slate_id = models.CharField(max_length=20)#Treat as string for now ... can't think of a downside at moment
    roster_position = models.CharField(max_length=20)
    salary = models.IntegerField()
    game_info = models.CharField(max_length=200)
    teamabbrev = models.CharField(max_length=20)
    avgpointspergame = models.DecimalField(max_digits=10, decimal_places=6)


