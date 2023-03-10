# Generated by Django 3.2.13 on 2022-06-18 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50, unique=True)),
                ('password', models.CharField(blank=True, max_length=50)),
                ('avatar', models.ImageField(default='account/avatar/null.png', upload_to='chat/avatar/')),
                ('fullname', models.CharField(blank=True, default='', max_length=100)),
                ('email', models.EmailField(blank=True, default='', max_length=100)),
                ('phone', models.CharField(blank=True, default='', max_length=20)),
                ('age', models.IntegerField(blank=True, default=0)),
            ],
        ),
    ]
