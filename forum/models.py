from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Topic(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    


class Room(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True, max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    #participants = 
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['-updated', '-created']#positive for ascending, - for descending



    def __str__(self):
        return self.name
    

#Many-to-one relationship. A post can only have one user, but a user can have many posts
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #A ForeignKey is a many-to-one relationship.
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    #models.CASCADE means when the room gets deleted, all messages are simply deleted. Altneratively, models.SET_NULL will set the messages to NULL (I think)
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.body[0:50]
    

    
