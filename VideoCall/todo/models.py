from django.db import models
from accounts.models import Account

# Create your models here.

class ToDoList(models.Model):
    title = models.CharField(max_length=100)
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.title}"

class ToDoItem(models.Model):
    title = models.CharField(max_length=255)
    todo_list = models.ForeignKey(ToDoList, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return f"{self.title}"