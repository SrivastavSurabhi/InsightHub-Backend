from django.db import models
from core.models import Genres
from people.models import Peoples
from django.utils import timezone

 

class Medias(models.Model):
    MediaType = (
        (1, 'Audio'),
        (2, 'Video'),
        (3, 'Podcast'),
    )
    mediaId = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=2000, null=True, blank=True)
    mediaImagePath = models.CharField(max_length=500, null=True, blank=True)
    authorName = models.CharField(max_length=200)
    mediaType = models.IntegerField(choices=MediaType)
    createdBy = models.IntegerField()
    createdOnUtc = models.DateTimeField(auto_now_add=True)
    modifiedBy = models.IntegerField()
    modifiedOnUtc = models.DateTimeField(auto_now=True)
    isDeleted = models.BooleanField(default=False)
    people = models.ManyToManyField(Peoples, through='MediaPeopleMapping',db_column='peopleId')
    genre = models.ManyToManyField(Genres, through='MediaGenreMapping',db_column='genreId')


class SubMedias(models.Model):
    subMediaId = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length = 200)
    description = models.CharField(max_length = 2000, null=True, blank=True)
    imagePath = models.CharField(max_length = 500, null=True, blank=True)
    fileUrl = models.CharField(max_length = 500)
    medias = models.ForeignKey(Medias, on_delete=models.CASCADE, related_name = 'subMedias', db_column='mediaId')
    viewsCount = models.IntegerField(default = 0)
    commentsCount = models.IntegerField(default = 0)
    likesCount = models.IntegerField(default = 0)
    dislikesCount = models.IntegerField(default = 0)
    createdBy = models.IntegerField()
    createdOnUtc = models.DateTimeField(auto_now_add=True)
    modifiedBy = models.IntegerField()
    modifiedOnUtc = models.DateTimeField(auto_now=True)
    isDeleted = models.BooleanField(default=False)
    publishedOn = models.DateTimeField()
    tags = models.ManyToManyField('SubMediasTags', related_name = 'subMediasTags', db_column='tagId')

class SubMediasTags(models.Model):
    tagId = models.BigAutoField(primary_key=True)
    subMediaId = models.ForeignKey(SubMedias, on_delete=models.CASCADE, related_name = 'subMediasTags', db_column='subMediaId')
    tagName = models.CharField(max_length = 200)
    createdBy = models.IntegerField()
    createdOnUtc = models.DateTimeField(auto_now_add=True)
    modifiedBy = models.IntegerField()
    modifiedOnUtc = models.DateTimeField(auto_now=True)
    isDeleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'medias_submediastags'

class MediaPeopleMapping(models.Model):
    mappingId = models.BigAutoField(primary_key=True)
    mediaId = models.ForeignKey(Medias, on_delete=models.CASCADE, related_name="mediapeople", db_column='mediaId')
    peopleId = models.ForeignKey(Peoples, on_delete=models.CASCADE, related_name = "peoplemedia", db_column='peopleId')
    createdBy = models.IntegerField()
    createdOnUtc = models.DateTimeField(auto_now_add=True)


class MediaGenreMapping(models.Model):
    mappingId = models.BigAutoField(primary_key=True)
    mediaId = models.ForeignKey(Medias, on_delete=models.CASCADE, related_name="mediagenre", db_column='mediaId')
    genreId = models.ForeignKey(Genres, on_delete=models.CASCADE, related_name="genremedia", db_column='genreId')
    createdBy = models.IntegerField()
    createdOnUtc = models.DateTimeField(auto_now_add=True)
