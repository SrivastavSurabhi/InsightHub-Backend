from django.db import models
from core.models import Genres

class Peoples(models.Model):
    peopleId = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length = 200)
    description = models.CharField(max_length = 2000,null=True, blank=True)
    profileImagePath = models.CharField(max_length = 500,null=True, blank=True)
    twitterHandle = models.CharField(max_length = 500,null=True, blank=True)
    youTubleChannelUrl = models.CharField(max_length = 1000,null=True, blank=True)
    createdBy = models.IntegerField()
    createdOnUtc = models.DateTimeField(auto_now_add=True)
    modifiedBy = models.IntegerField()
    modifiedOnUtc = models.DateTimeField(auto_now=True)
    isDeleted = models.BooleanField(default=False)
    isFeatured = models.BooleanField(default=False)
    bannerImagePath = models.CharField(max_length = 1000,null=True, blank=True)
    bannerProfileImagePath = models.CharField(max_length = 1000,null=True, blank=True)
    genre = models.ManyToManyField(Genres, through="PeopleGenreMapping",db_column='genreId')

class PeopleGenreMapping(models.Model):
    mappingId = models.BigAutoField(primary_key=True)
    peopleId = models.ForeignKey(Peoples, on_delete=models.CASCADE,db_column='peopleId')
    genreId = models.ForeignKey(Genres, on_delete=models.CASCADE,db_column='genreId')
    createdBy = models.IntegerField()
    createdOnUtc = models.DateTimeField(auto_now_add=True)