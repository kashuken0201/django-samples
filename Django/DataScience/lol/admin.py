from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Champion)
admin.site.register(Game)
admin.site.register(GamePlay)
admin.site.register(Lane)
admin.site.register(Team)