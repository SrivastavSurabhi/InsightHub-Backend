from rest_framework import serializers
from .models import *
from people.serializers import PeopleSerializer
from django.db.models import F

class TweetsSerializer(serializers.ModelSerializer):
    tweetedByPersonId = PeopleSerializer(many=False)
    class Meta:
        model = Tweets
        fields = ['tweetId', 'externalTweetId', 'tweet', 'isRetweeted', 'parentRetweetedId', 'tweetedBy',
                  'tweetedByPersonId', 'tweetedOn', 'retweetsCount', 'likesCount', 'repliesCount']

class MostRetweetedSerializer(serializers.ModelSerializer):
    tweetedByPersonId = PeopleSerializer(many=False)
    parentRetweet = serializers.SerializerMethodField()
    class Meta:
        model = Tweets
        fields = ['tweetId', 'externalTweetId', 'tweet', 'isRetweeted', 'parentRetweetedId','parentRetweet', 
                'tweetedBy','tweetedByPersonId', 'tweetedOn', 'retweetsCount', 'likesCount', 'repliesCount']

    def get_parentRetweet(self, obj):
        try:
            value = Tweets.objects.annotate(tweetedByPersonName=F('tweetedByPersonId__name'),\
                tweetedByPersonProfileImage = F('tweetedByPersonId__profileImagePath')).values('tweetId',\
                'externalTweetId', 'tweet', 'isRetweeted','parentRetweetedId', 'tweetedBy',\
                'tweetedByPersonId','tweetedByPersonName','tweetedByPersonProfileImage','tweetedOn',
                'retweetsCount','likesCount', 'repliesCount').get(externalTweetId = obj.parentRetweetedId)
            return value
        except:
            return {}


class CreateTweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweets
        fields = ['tweetId', 'externalTweetId', 'tweet', 'isRetweeted', 'parentRetweetedId', 'tweetedBy',
                  'tweetedByPersonId', 'tweetedOn', 'retweetsCount', 'likesCount', 'repliesCount','createdBy','modifiedBy']

    def create(self, validated_data):
        return Tweets.objects.create(**validated_data)
