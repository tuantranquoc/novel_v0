# Generated by Django 3.0.7 on 2021-03-09 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('novel', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='view',
            name='novel',
        ),
        migrations.RemoveField(
            model_name='view',
            name='user',
        ),
        migrations.RemoveField(
            model_name='novel',
            name='bookmark',
        ),
        migrations.RemoveField(
            model_name='novel',
            name='recommend',
        ),
        migrations.AddField(
            model_name='novel',
            name='save_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='novel',
            name='view_count',
            field=models.IntegerField(default=0),
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
        migrations.DeleteModel(
            name='View',
        ),
    ]
