# Generated by Django 3.0.2 on 2020-03-26 15:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('grades', '0013_assignment_pointbased'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='assignment',
            name='pointbased',
        ),
    ]
