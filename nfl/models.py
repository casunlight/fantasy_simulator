from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Player(models.Model):
    name=models.CharField(max_length=100, null=True)
    name_id = models.CharField(max_length=100, null=True)
    salary = models.IntegerField(null=True)
    position = models.CharField(max_length=100, null=True)
    proj = models.DecimalField(max_digits=7, decimal_places=3, null=True)
    
  
