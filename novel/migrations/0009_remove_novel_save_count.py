# Generated by Django 3.0.7 on 2021-03-09 07:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('novel', '0008_novel_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='novel',
            name='save_count',
        ),
    ]
