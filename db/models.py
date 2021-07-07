from django.utils.timezone import now
from django.db import models


class TopicCategory(models.Model):
    id = models.AutoField(primary_key=True)
    topicId = models.TextField(unique=True)
    wiki = models.TextField()


class Channel(models.Model):
    id = models.CharField(max_length=30, primary_key=True)
    title = models.TextField(default="")
    publishedAt = models.DateTimeField(default=now)

    country = models.CharField(max_length=3, null=True)
    topics = models.ManyToManyField(TopicCategory)

    fetched = models.DateTimeField(default=now)


class Statistic(models.Model):
    id = models.OneToOneField(Channel, on_delete=models.CASCADE, primary_key=True)
    viewCount = models.BigIntegerField(default=0)
    subscriberCount = models.IntegerField(default=0)
    hiddenSubscriberCount = models.BooleanField(default=False)
    videoCount = models.IntegerField(default=0)

