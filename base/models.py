from django.db import models

# Create your models here.

class Room(models.Model):
    #host 
    #topic
    name = models.CharField(max_length=200)
    description = models.TextField(null=True , blank=True)
    #participants . 
    updated = models.DateTimeField(auto_now=True) #last time created /updated . 
    created = models.DateTimeField(auto_now_add=True) # store time created . // only 1 time occurs 

    def __str__(self):
        return self.name 
    
class Message(models.Model):

    room = models.ForeignKey(Room , on_delete=models.CASCADE) # cascde means-->delete all messages in room if we delete room . 
    body = models.TextField()
    updated = models.DateTimeField(auto_now=T)