# create serializer for semantic search
from rest_framework import serializers
from .models import *
class SemanticSearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = SemanticSearch
        fields = ['id', 'start', 'end', 'video_id', 'text', 'score', 'subMediaId', 'name', 'description', 'imagePath', 'fileUrl', 'peopleId', 'peopleName', 'profileImagePath', 'viewsCount', 'likesCount', 'dislikesCount', 'commentsCount']
