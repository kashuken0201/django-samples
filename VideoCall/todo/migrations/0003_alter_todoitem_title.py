# Generated by Django 3.2.13 on 2022-06-18 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0002_alter_todoitem_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todoitem',
            name='title',
            field=models.CharField(max_length=255),
        ),
    ]
