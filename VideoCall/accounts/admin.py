from django.contrib import admin
from .models import *

# Register your models here.
class AccountAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'password']  

admin.site.register(Account, AccountAdmin)