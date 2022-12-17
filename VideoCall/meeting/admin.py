from django.contrib import admin
from .models import *

# Register your models here.
class RoomAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
   
class MemberAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'room']

admin.site.register(Room, RoomAdmin)
admin.site.register(Member, MemberAdmin)