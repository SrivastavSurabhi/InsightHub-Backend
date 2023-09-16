from rest_framework import serializers
from .models import *
from core.serializers import *
from django.db import transaction


class PeopleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Peoples
        fields = ['peopleId', 'name', 'description', 'profileImagePath', 'twitterHandle', 'youTubleChannelUrl']

class PeopleCreateSerializer(serializers.ModelSerializer):

    genre = GenreSerializer(read_only=True,many=True)
    genres = serializers.PrimaryKeyRelatedField(queryset=Genres.objects.all(), write_only=True,many=True)

    class Meta:
        model = Peoples
        fields = ['peopleId','name', 'description', 'profileImagePath', 'twitterHandle', 'youTubleChannelUrl','createdBy',
                  'modifiedBy','isFeatured','bannerImagePath','bannerProfileImagePath','genre','genres']

    def create(self, validated_data):
        with transaction.atomic():
            genre = validated_data.pop("genres")
            people = Peoples.objects.create(**validated_data)
            for gen in genre:
                PeopleGenreMapping.objects.create(peopleId=people, genreId=gen, createdBy=gen.createdBy)
            return people

class PeopleDetailSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True)
    class Meta:
        model = Peoples
        fields = ['peopleId', 'name', 'description', 'profileImagePath', 'twitterHandle', 'youTubleChannelUrl','bannerImagePath','bannerProfileImagePath', 'genre']
        depth = 1
