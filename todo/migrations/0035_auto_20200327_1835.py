# Generated by Django 3.0.4 on 2020-03-27 22:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0034_auto_20200325_1834'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='due_date',
            field=models.DateField(default=datetime.datetime(2020, 3, 27, 18, 35, 44, 618417)),
        ),
    ]