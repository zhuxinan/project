# Generated by Django 2.2 on 2019-05-09 02:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_auto_20190508_1732'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='collections',
            name='cduration',
        ),
        migrations.RemoveField(
            model_name='collections',
            name='cimage',
        ),
        migrations.RemoveField(
            model_name='collections',
            name='ctitle',
        ),
        migrations.AddField(
            model_name='collections',
            name='mid',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='movies.Movies'),
        ),
    ]
