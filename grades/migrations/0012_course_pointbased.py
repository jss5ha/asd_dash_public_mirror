# Generated by Django 3.0.2 on 2020-03-26 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grades', '0011_auto_20200306_2016'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='pointbased',
            field=models.BooleanField(default=False),
        ),
    ]