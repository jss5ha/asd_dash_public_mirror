# Generated by Django 3.0.2 on 2020-03-07 00:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('grades', '0007_auto_20200306_1900'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='ass_type',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='grades.assType'),
        ),
    ]