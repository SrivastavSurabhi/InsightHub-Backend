from django.db import models

#create model class
class SemanticSearch(models.Model):
    id = models.BigAutoField(primary_key=True)
    start = models.FloatField(default=0)
    end = models.FloatField(default=0)
    video_id = models.CharField(max_length=2000, null=True, blank=True)
    text = models.CharField(max_length=2000, null=True, blank=True)
    score = models.FloatField(default=0)
    subMediaId = models.CharField(max_length=2000, null=True, blank=True)
    name = models.CharField(max_length=2000, null=True, blank=True)
    description = models.CharField(max_length=2000, null=True, blank=True)
    imagePath = models.CharField(max_length=2000, null=True, blank=True)
    fileUrl = models.CharField(max_length=2000, null=True, blank=True)
    peopleId = models.CharField(max_length=2000, null=True, blank=True)
    profileImagePath = models.CharField(max_length=2000, null=True, blank=True)
    viewsCount = models.CharField(max_length=2000, null=True, blank=True)
    likesCount = models.CharField(max_length=2000, null=True, blank=True)
    dislikesCount = models.CharField(max_length=2000, null=True, blank=True)
    commentsCount = models.CharField(max_length=2000, null=True, blank=True)
    peopleName = models.CharField(max_length=2000, null=True, blank=True)

