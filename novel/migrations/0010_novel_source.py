# Generated by Django 3.0.7 on 2021-03-09 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('novel', '0009_remove_novel_save_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='novel',
            name='source',
            field=models.TextField(default='source require'),
        ),
    ]
