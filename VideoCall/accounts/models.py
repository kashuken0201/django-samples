from django.db import models

class Account(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=50, blank=True)
    
    avatar = models.ImageField(upload_to='accounts/avatar/', default= 'accounts/avatar/null.png', blank=False)
    fullname = models.CharField(max_length=100, default='', blank=True)
    email = models.EmailField(max_length=100, default='', blank=True)
    phone = models.CharField(max_length=20, default='', blank=True)
    age = models.IntegerField(default=0, blank=True)
    
    def __str__(self) -> str:
        return f'{self.username}'
    