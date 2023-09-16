from pickle import TRUE
from rest_framework import serializers
from .models import *
from people.serializers import *
from core.serializers import *


class MediaPeopleSerializer(serializers.ModelSerializer):
    people = PeopleSerializer(many=True)
    class Meta:
        model = Medias
        fields = ['mediaId', 'mediaType', 'people']

class SubMediaTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubMediasTags
        fields = ['tagId','subMediaId','tagName']

class SubMediaTagCountSerializer(serializers.Serializer):
    tagName = serializers.CharField()
    tagCount = serializers.IntegerField()

    def to_representation(self, instance):
        return {
            'tagName': instance['tagName'],
            'tagCount': instance['tagCount']
        }

class SubMediaSerializer(serializers.ModelSerializer):
    medias = MediaPeopleSerializer(many=False)
    class Meta:
        model = SubMedias
        fields = ['subMediaId','name','description','imagePath','fileUrl','medias','viewsCount','commentsCount','likesCount','dislikesCount', 'publishedOn']


class MediaSerializer(serializers.ModelSerializer):
    subMedias = SubMediaSerializer(many=True)
    class Meta:
        model = Medias
        fields = ['mediaId','name','description','mediaImagePath','authorName','mediaType','subMedias']


class MediaDetailSerializer(serializers.ModelSerializer):
    subMedias = SubMediaSerializer(many=True)
    people = PeopleSerializer(many=True)
    genre = GenreSerializer(many=True)
    class Meta:
        model = Medias
        fields = ['mediaId','name','description','mediaImagePath','authorName','mediaType','people','genre','subMedias']
        depth = 1


class CreateMediaSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    genres = serializers.PrimaryKeyRelatedField(many=True, write_only=True, queryset=Genres.objects.all())
    people = PeopleSerializer(many=True, read_only=True)
    peoples = serializers.PrimaryKeyRelatedField(many=True, write_only=True, queryset=Peoples.objects.all())
    class Meta:
        model = Medias
        fields = ['mediaId','name', 'description', 'mediaImagePath', 'authorName', 'mediaType', 'createdBy', 'modifiedBy',
                  'people', 'peoples', 'genre', 'genres']

    def create(self, validated_data):
        genre = validated_data.pop("genres")
        people = validated_data.pop("peoples")
        media = Medias.objects.create(**validated_data)
        for g in genre:
            MediaGenreMapping.objects.create(mediaId=media, genreId=g, createdBy=1)
        for p in people:
            MediaPeopleMapping.objects.create(mediaId=media, peopleId=p, createdBy=1)
        return media


class CreateSubMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubMedias
        fields = ['subMediaId','name', 'description', 'imagePath', 'fileUrl', 'medias', 'viewsCount', 'commentsCount',
                  'createdBy', 'modifiedBy','likesCount', 'dislikesCount', 'publishedOn']

    def validate_fileUrl(self, value):
        """
        Check if fileUrl is already exists.
        """
        if SubMedias.objects.filter(fileUrl=value).exists():
            raise serializers.ValidationError("fileUrl already exists.")
        return value

    def create(self, validated_data):
        submedia = SubMedias.objects.create(**validated_data)
        return submedia

class CreateSubMediaTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubMediasTags
        fields = ['tagId','subMediaId','tagName','createdBy', 'modifiedBy']
    def create(self, validated_data):
        submediatag = SubMediasTags.objects.create(**validated_data)
        return submediatag


class SearchSubMediaSerializer(serializers.ModelSerializer):
    
    medias = MediaPeopleSerializer(many=False)    

    class Meta:
        model = SubMedias
        fields = ['subMediaId','name','description','imagePath','fileUrl', 'medias','viewsCount','commentsCount','likesCount','dislikesCount']


class MediaSpeificSerializer(serializers.ModelSerializer):
    class Meta:
        model =Medias
        fields = ['mediaId','name','mediaType']


class FeaturedMediaSerializer(serializers.ModelSerializer):
    medias = MediaSpeificSerializer(many=False)    
    class Meta:
        model = SubMedias
        fields = ['subMediaId','name','description','imagePath','fileUrl', 'medias','viewsCount','commentsCount','likesCount','dislikesCount']

