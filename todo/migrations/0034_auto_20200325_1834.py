# Generated by Django 3.0.4 on 2020-03-25 22:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0033_auto_20200325_1612'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='due_date',
            field=models.DateField(default=datetime.datetime(2020, 3, 25, 18, 34, 19, 523965)),
        ),
    ]