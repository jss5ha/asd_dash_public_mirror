# Generated by Django 3.0.2 on 2020-04-08 00:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calendarMod', '0004_event_from_google'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='minute',
            field=models.TextField(default=''),
        ),
    ]
