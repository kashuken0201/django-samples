from django.db import models

# Create your models here.
class Room(models.Model):
    room_name = models.TextField(
        max_length=255, 
        null=False
    )

    def __str__(self) -> str:
        return f'{self.room_name}'

class Facilities(models.Model):
    facility_name = models.TextField(max_length=255)
    quantity = models.IntegerField()

    room = models.ForeignKey(
        Room,
        on_delete=models.CASCADE,
        blank=False,
        null=False
    )

    


