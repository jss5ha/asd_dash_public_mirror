# Generated by Django 3.0.2 on 2020-04-08 00:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calendarMod', '0005_event_minute'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='minute',
            new_name='startminute',
        ),
        migrations.AddField(
            model_name='event',
            name='endminute',
            field=models.TextField(default=''),
        ),
    ]