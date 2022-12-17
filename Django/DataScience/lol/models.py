from django.db import models

# Create your models here.

class Champion(models.Model):
    champ_id = models.IntegerField(primary_key=True)
    champ_name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f'{self.champ_id} - {self.champ_name}'

class Lane(models.Model):
    lane_id = models.IntegerField(primary_key=True)
    lane_name = models.CharField(max_length=50)

class Team(models.Model):
    team_id = models.IntegerField(primary_key=True)
    team_name = models.CharField(max_length=30)

class Game(models.Model):
    game_id = models.IntegerField(primary_key=True)
    team_win_id = models.ForeignKey(Team, on_delete=models.CASCADE)

class GamePlay(models.Model):
    game_play_id = models.IntegerField(primary_key=True)
    game_id = models.ForeignKey(Game, on_delete=models.CASCADE)
    champ_id = models.ForeignKey(Champion, on_delete=models.CASCADE)
    team_id = models.ForeignKey(Team, on_delete=models.CASCADE)
    lane_id = models.ForeignKey(Lane, on_delete=models.CASCADE)

