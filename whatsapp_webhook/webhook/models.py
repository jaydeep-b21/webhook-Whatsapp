# Create your models here.
from django.db import models
 
class Message(models.Model):
    sender = models.CharField(max_length=255)
    receiver = models.CharField(max_length=255)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default="Pending")
    mobile_no=models.CharField(max_length=12,null=True)
 
    def __str__(self):
        return self.sender