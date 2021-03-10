# Generated by Django 3.0.7 on 2021-03-09 11:07

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('novel', '0011_auto_20210309_1635'),
    ]

    operations = [
        migrations.AddField(
            model_name='chapter',
            name='chapter_number',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='chapter',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='chapter',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='novel',
            name='public',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='novel',
            name='removed',
            field=models.BooleanField(default=True),
        ),
    ]