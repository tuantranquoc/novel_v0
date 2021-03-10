from django.db import models
from django.db.models import Model
from novel import choice
from django.utils import timezone

# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name


class Novel(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    status = models.IntegerField(choices=choice.STATUS_CHOICES, default=1)
    category = models.ManyToManyField(
        Category, blank=True)
    view_count = models.CharField(max_length=255, blank=True, null=True)
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now_add=True)
    number_of_chapter = models.IntegerField(default=0)
    slug = models.CharField(max_length=255, blank=True, null=True)
    source = models.TextField(default="source require")
    # public, removed
    public = models.BooleanField(default=False)
    removed = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Chapter(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    novel = models.ForeignKey(
        Novel, on_delete=models.CASCADE, blank=True, null=True)
    content = models.TextField()
    # created_at, updated_at, num
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    chapter_number = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title

# class View(models.Model):
#     user = models.ForeignKey(
#         User, on_delete=models.CASCADE, blank=True, null=True)
#     novel = models.ForeignKey(
#         Novel, on_delete=models.CASCADE, blank=True, null=True)
#     last_access_date = models.DateTimeField(default=timezone.now)
#     count = models.IntegerField(default=0)


# class Comment(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     content = models.TextField(blank=True)
#     timestamp = models.DateTimeField(auto_now_add=True)
#     parent = models.ForeignKey('self',
#                                null=True,
#                                on_delete=models.CASCADE,
#                                blank=True)
#     novel = models.ForeignKey(Novel,
#                              on_delete=models.CASCADE,
#                              null=True,
#                              blank=True)
#     up_vote = models.ManyToManyField(User,
#                                      related_name="c_up_vote",
#                                      blank=True)
#     level = models.IntegerField(default=1)
#     state = models.CharField(blank=False,
#                              null=True,
#                              max_length=10,
#                              default='public')
