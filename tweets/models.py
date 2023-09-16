from django.db import models
from people.models import Peoples

# Create your models here.
class Tweets(models.Model):
    tweetId = models.BigAutoField(primary_key=True)
    externalTweetId = models.BigIntegerField()
    tweet = models.CharField(max_length=2000, null=True, blank=True)
    isRetweeted = models.BooleanField(default=False)
    parentRetweetedId = models.BigIntegerField(null=True, blank=True)
    tweetedBy = models.CharField(max_length=200)
    tweetedByPersonId = models.ForeignKey(Peoples, on_delete=models.CASCADE, null=True,db_column='tweetedByPersonId')
    tweetedOn = models.DateTimeField()
    retweetsCount = models.IntegerField(default=0)
    likesCount = models.IntegerField(default=0)
    repliesCount = models.IntegerField(default=0)
    createdBy = models.IntegerField()
    createdOnUtc = models.DateTimeField(auto_now_add=True)
    modifiedBy = models.IntegerField()
    modifiedOnUtc = models.DateTimeField(auto_now=True)
    isDeleted = models.BooleanField(default=False)
