from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['userRole'] = user.userRole
        return token
class GenreSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Genres
        fields = ['genreId','name','description','genreImagePath']


class GenreCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genres
        fields = ['genreId','name','description','genreImagePath','genreType','createdBy','modifiedBy']

    def create(self, validated_data):
        return Genres.objects.create(**validated_data)