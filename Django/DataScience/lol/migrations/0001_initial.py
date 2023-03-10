# Generated by Django 4.0.1 on 2022-06-30 04:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Champion',
            fields=[
                ('champ_id', models.IntegerField(primary_key=True, serialize=False)),
                ('champ_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('game_id', models.IntegerField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Lane',
            fields=[
                ('lane_id', models.IntegerField(primary_key=True, serialize=False)),
                ('lane_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('team_id', models.IntegerField(primary_key=True, serialize=False)),
                ('team_name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='GamePlay',
            fields=[
                ('game_play_id', models.IntegerField(primary_key=True, serialize=False)),
                ('champ_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lol.champion')),
                ('game_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lol.game')),
                ('lane_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lol.lane')),
                ('team_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lol.team')),
            ],
        ),
        migrations.AddField(
            model_name='game',
            name='team_win_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lol.team'),
        ),
    ]
