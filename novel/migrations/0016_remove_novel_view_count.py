# Generated by Django 3.0.7 on 2021-03-12 16:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('novel', '0015_auto_20210310_2104'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='novel',
            name='view_count',
        ),
    ]
