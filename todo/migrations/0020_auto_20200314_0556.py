# Generated by Django 3.0.2 on 2020-03-14 09:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0019_auto_20200306_2016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='due_date',
            field=models.DateField(default=datetime.datetime(2020, 3, 14, 5, 56, 36, 839233)),
        ),
    ]
