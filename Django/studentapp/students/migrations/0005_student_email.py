# Generated by Django 4.0.3 on 2022-05-05 03:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0004_alter_student_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='email',
            field=models.TextField(null=True),
        ),
    ]
