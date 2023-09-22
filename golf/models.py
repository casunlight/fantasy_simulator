from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Golfer(models.Model):
    name=models.CharField(max_length=100, null=True)
    name_id = models.CharField(max_length=100, null=True)
    salary = models.IntegerField(null=True)
    proj = models.DecimalField(max_digits=7, decimal_places=3, null=True)
    #opto_exclude = models.BooleanField(default=False, null=True)
    #opto_like = models.BooleanField(default=False, null=True)



class Lineup(models.Model):
    proj = models.DecimalField(max_digits=5, decimal_places=3, null=True)
    salary = models.IntegerField(null=True)
    #thinking of storing as json for now, can revisit
    players = models.CharField(max_length=1000, null=True)
    #which user made this lineup/set of lineups
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="optimized_lineups", default=1000, null=True)
#    pass

