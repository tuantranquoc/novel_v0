# Generated by Django 3.0.7 on 2021-03-09 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('novel', '0004_novel_bookmark_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='novel',
            name='number_of_chapter',
            field=models.IntegerField(default=0),
        ),
    ]
