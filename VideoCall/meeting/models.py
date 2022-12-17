from django.db import models
from accounts.models import Account

# Create your models here.
class Room(models.Model):
    name = models.TextField(max_length=255)
    password = models.CharField(max_length=50, blank=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f'{self.name}'
     
class Member(models.Model):
    name = models.TextField(max_length=255)
    room = models.ForeignKey(
        Room, 
        on_delete=models.CASCADE,
        null=True)

    def __str__(self):
        return self.name