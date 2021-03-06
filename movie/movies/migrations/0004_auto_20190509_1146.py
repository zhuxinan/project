# Generated by Django 2.2 on 2019-05-09 03:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0003_auto_20190509_1007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collections',
            name='mid',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='movies.Movies', unique=True),
        ),
        migrations.AlterField(
            model_name='movies',
            name='title',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
