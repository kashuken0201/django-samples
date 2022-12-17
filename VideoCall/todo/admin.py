from django.contrib import admin
from .models import *

# Register your models here.
class ToDoListAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_display = ['id', 'title', 'user']

class ToDoItemAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_display = ['id', 'title', 'todo_list']

admin.site.register(ToDoItem, ToDoItemAdmin)
admin.site.register(ToDoList, ToDoListAdmin)