from django.db import models

from django.contrib.auth.models import User
# Create your models here.

class Topic(models.Model):#one topic can have many rooms , but room has one topic only . 
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Room(models.Model):
    host  = models.ForeignKey(User,on_delete=models.SET_NULL , null=True)#foreign key means koi dusra model as value here , // yha User model use kr rhe h .  
    topic = models.ForeignKey(Topic , on_delete=models.SET_NULL , null=True) # if topic deleted set null & allow room to be null .
    name = models.CharField(max_length=200)
    description = models.TextField(null=True , blank=True)
    #participants . 
    updated = models.DateTimeField(auto_now=True) #last time created /updated . 
    created = models.DateTimeField(auto_now_add=True) # store time created . // only 1 time occurs .


    class Meta:
        ordering =['-updated' , '-created'] # now it will prioritized  or stored & showed   as newest first in ascending order 
        # remove - to reverse order like , ordering = ['updated']
    def __str__(self):
        return self.name 
    
class Message(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    room = models.ForeignKey(Room , on_delete=models.CASCADE) # cascde means-->delete all messages in room if we delete room . 
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)


'''
But Django automatically creates a reverse relationship from Room to Message because of this line in your Message model:

room = models.ForeignKey(Room, on_delete=models.CASCADE)


******When you write this in your Message model:

room = models.ForeignKey(Room, on_delete=models.CASCADE)
You're saying:
“Each message belongs to one room.”

But Django also gives you something extra automatically:

It creates a reverse link — so from a Room object, you can find all the messages related to it.

'''