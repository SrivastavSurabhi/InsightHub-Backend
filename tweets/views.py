from InsightHubAPI.common_import import *
from .serializers import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from django.db.models import Q
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.pagination import LimitOffsetPagination
from collections import OrderedDict
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers

class TweetsView(APIView, LimitOffsetPagination):
    __doc__ = """ Get All Tweets or Particular Tweet Info"""
    permission_classes = [HasAPIKey]
    pagination_class = pagination_settings.DEFAULT_PAGINATION_CLASS

    def get_all_tweets(self):
        return Tweets.objects.filter(Q(isDeleted=False), ~Q(parentRetweetedId=None),\
             Q(parentRetweetedId__gt = 0)).order_by('-tweetedOn')

    def get_tweet_by_id(self, id):
        try:
            return Tweets.objects.get(tweetId=id, isDeleted=False)
        except Tweets.DoesNotExist:
            raise Http404

    @method_decorator(cache_page(60*60*2))
    @method_decorator(vary_on_headers("Authorization"))
    def get(self, request, *args, **kwargs):
        try:
            people_id = int(kwargs['id'])
        except:
            people_id = 0

        if people_id > 0:
            people = self.get_tweet_by_id(people_id)
            serializer = TweetsSerializer(people, many=False)
        else:
            tweets = self.get_all_tweets()
            results = self.paginate_queryset(tweets, request, view=self)
            if results is not None:
                serializer =  TweetsSerializer(results, many=True)   
                return Response(OrderedDict([('count', self.count),('data', serializer.data)]))
            else:
                serializer = TweetsSerializer(tweets, many=True) 
                return Response({"count":tweets.count(),"data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    
class CreateTweetsView(APIView):
    __doc__ = """For add new people"""
    serializer_class = CreateTweetSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,IsAdminUser]
    pagination_class = pagination_settings.DEFAULT_PAGINATION_CLASS

    def post(self, request, *args, **kwargs):
        data = request.data
        user = request.user.id
        data['createdBy'] = data['modifiedBy']= user
        serializer = self.serializer_class(data=data)
        return commonPostApi(serializer)


class DeleteTweetsView(APIView):
    __doc__ = """For delete people"""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,IsAdminUser]

    def delete(self, request, tweet_id, *args, **kwargs):
        return commonDeleteApi(Tweets, tweet_id)


class MostRetweetedTweetsView(APIView,LimitOffsetPagination):
    __doc__ = """Most Retweeted API"""
    permission_classes = [HasAPIKey]
    pagination_class = LimitOffsetPagination

    @method_decorator(cache_page(60*60*2))
    @method_decorator(vary_on_headers("Authorization"))
    def get(self, request, *args, **kwargs):
        tweets = Tweets.objects.filter(Q(isDeleted=False), ~Q(parentRetweetedId=None),\
                Q(parentRetweetedId__gt = 0)).order_by('-retweetsCount')
        results = self.paginate_queryset(tweets, request, view=self)
        if results is not None:
            serializer =  MostRetweetedSerializer(results, many=True)   
            return Response(OrderedDict([('count', self.count),('data', serializer.data)]))
        else:
            serializer = MostRetweetedSerializer(tweets, many=True) 
            return Response({"count":tweets.count(),"data": serializer.data}, status=status.HTTP_200_OK)


class MostRetweetedTweetsByPeopleIdView(APIView,LimitOffsetPagination):
    __doc__ = """Most Retweeted API by PeopleId"""
    permission_classes = [HasAPIKey]
    pagination_class = LimitOffsetPagination

    @method_decorator(cache_page(60*60*2))
    @method_decorator(vary_on_headers("Authorization"))
    def get(self, request, *args, **kwargs):
        peopleId = kwargs['peopleId']
        tweets = Tweets.objects.filter(Q(isDeleted=False), Q(tweetedByPersonId = peopleId),\
                ~Q(parentRetweetedId=None),Q(parentRetweetedId__gt = 0)).order_by('-retweetsCount')
        results = self.paginate_queryset(tweets, request, view=self)
        if results is not None:
            serializer =  MostRetweetedSerializer(results, many=True)   
            return Response(OrderedDict([('count', self.count),('data', serializer.data)]))
        else:
            serializer = MostRetweetedSerializer(tweets, many=True) 
            return Response({"count":tweets.count(),"data": serializer.data}, status=status.HTTP_200_OK)