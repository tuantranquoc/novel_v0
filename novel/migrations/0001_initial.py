# Generated by Django 3.0.7 on 2021-03-09 04:28

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('content', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Novel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('status', models.IntegerField(choices=[(1, 'Đang ra'), (2, 'Full')], default=1)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='View',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_access_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('count', models.IntegerField(default=0)),
                ('novel', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='novel.Novel')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='novel.User')),
            ],
        ),
        migrations.AddField(
            model_name='novel',
            name='bookmark',
            field=models.ManyToManyField(blank=True, related_name='bookmark', to='novel.User'),
        ),
        migrations.AddField(
            model_name='novel',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='novel.Category'),
        ),
        migrations.AddField(
            model_name='novel',
            name='chapter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='novel.Chapter'),
        ),
        migrations.AddField(
            model_name='novel',
            name='recommend',
            field=models.ManyToManyField(blank=True, to='novel.User'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(blank=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('level', models.IntegerField(default=1)),
                ('state', models.CharField(default='public', max_length=10, null=True)),
                ('novel', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='novel.Novel')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='novel.Comment')),
                ('up_vote', models.ManyToManyField(blank=True, related_name='c_up_vote', to='novel.User')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='novel.User')),
            ],
        ),
    ]
