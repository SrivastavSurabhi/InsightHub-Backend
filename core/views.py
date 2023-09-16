from InsightHubAPI.common_import import *
from .serializers import *
from medias.models import *
from medias.serializers import * 
from tweets.models import *
from tweets.views import *
from people.models import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)
from InsightHubAPI import errors
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework_api_key.models import APIKey
import datetime
from rest_framework.pagination import LimitOffsetPagination
from collections import OrderedDict
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers


# api_key, key = APIKey.objects.create_key(name="my-remote-service")


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    token_obtain_pair = TokenObtainPairView.as_view()
    permission_classes = [AllowAny]


class APITokenView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    @method_decorator(cache_page(60*60*2))
    @method_decorator(vary_on_headers("Authorization"))
    def get(self,request, *args, **kwargs):
        todaysdate = datetime.datetime.now()
        expiry_date = todaysdate.replace(year=todaysdate.year + 20)
        api_key, key = APIKey.objects.create_key(name="my-api-key",expiry_date = expiry_date )
        return Response({'api-key':key})


class GenreView(APIView,LimitOffsetPagination):
    __doc__ = """ Get All Genre """
    permission_classes = [HasAPIKey]
    pagination_class = LimitOffsetPagination

    def get_all_genre(self):
        return Genres.objects.filter(isDeleted=False).order_by('-genreId')
    
    @method_decorator(cache_page(60*60*2))
    @method_decorator(vary_on_headers("Authorization"))
    def get(self,request, *args, **kwargs):
        genre = self.get_all_genre()
        results = self.paginate_queryset(genre, request, view=self)
        if results is not None:
            serializer =  GenreSerializer(results, many=True)   
            return Response(OrderedDict([('count', self.count),('data', serializer.data)]))
        else:
            serializer = GenreSerializer(genre, many=True) 
            return Response({"count":genre.count(),"data": serializer.data}, status=status.HTTP_200_OK)

class CreateGenreView(APIView):
    __doc__ = """For add new genre"""
    serializer_class = GenreCreateSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request, *args, **kwargs):
        genreChoice = [1, 2]
        data = request.data
        userId = request.user.id
        data['createdBy'] = data['modifiedBy'] = userId
        serializer = self.serializer_class(data=data)
        try:
            genreType = request.data['genreType']
        except:
            genreType = None
        if genreType not in genreChoice and genreType != None:
            raise serializers.ValidationError({'genreType':errors.GENRETYPE}, code=status.HTTP_400_BAD_REQUEST)
        return commonPostApi(serializer)


class DeleteGenreView(APIView):
    __doc__ = """For delete genre"""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def delete(self, request, genre_id, *args, **kwargs):
        return commonDeleteApi(Genres, genre_id)


class SearchView(APIView,LimitOffsetPagination):
    __doc__ = """ Global Search API"""
    permission_classes = [HasAPIKey]
    pagination_class = pagination_settings.DEFAULT_PAGINATION_CLASS

    @method_decorator(cache_page(60*60*2))
    @method_decorator(vary_on_headers("Authorization"))
    def get(self, request, *args, **kwargs):
        search = kwargs['Search']
        search_submedia = SubMedias.objects.filter(name__icontains = search, isDeleted=False)
        search_people = Peoples.objects.filter(name__icontains = search, isDeleted=False)
        search_tweets = Tweets.objects.filter(tweet__icontains = search, isDeleted=False)
        search_retweets = Tweets.objects.filter(Q(tweet__icontains = search),Q(isDeleted=False),\
            ~Q(parentRetweetedId=None),Q(parentRetweetedId__gt = 0))
        submedia_serializer = SearchSubMediaSerializer(search_submedia, many=True)
        people_serializer = PeopleSerializer(search_people, many=True)
        tweets_serializer = TweetsSerializer(search_tweets, many=True)   
        retweets_serializer = MostRetweetedSerializer(search_retweets, many=True)   
        return Response({"search_submedia":submedia_serializer.data,\
                         "search_people":people_serializer.data,\
                         "search_tweet" : tweets_serializer.data,\
                         "search_retweet" :  retweets_serializer.data\
                            }, status=status.HTTP_200_OK)


class GetDataByGenreIdView(APIView):
    __doc__ = """ Global Data By Genre Id API"""
    permission_classes = [HasAPIKey]
    pagination_class = pagination_settings.DEFAULT_PAGINATION_CLASS

    @method_decorator(cache_page(60*60*2))
    @method_decorator(vary_on_headers("Authorization"))
    def get(self, request, *args, **kwargs):
        genreId = kwargs['genre_id']
        peoples = Peoples.objects.filter(peoplegenremapping__genreId = genreId).distinct()
        people_serializer = PeopleSerializer(peoples, many=True)
        return Response({"peoples":people_serializer.data}, status=status.HTTP_200_OK)


class SearchPostView(APIView):
    __doc__ = """ Global Search POST API"""
    permission_classes = [HasAPIKey]
    pagination_class = pagination_settings.DEFAULT_PAGINATION_CLASS


    def post(self, request, *args, **kwargs):
        search = request.data['query']
        search_submedia = SubMedias.objects.filter(name__icontains = search, isDeleted=False)
        search_people = Peoples.objects.filter(name__icontains = search, isDeleted=False)
        try:    
            genres = request.data['genres']
            if genres != None and len(genres) > 0:
                search_people = search_people.filter(genre__in = genres).distinct()
                search_submedia = search_submedia.filter(medias__genre__in = genres).distinct()
        except:
            pass
        submedia_serializer = SearchSubMediaSerializer(search_submedia, many=True)
        people_serializer = PeopleSerializer(search_people, many=True)
        
        return Response({"search_submedia":submedia_serializer.data,\
                "search_people":people_serializer.data,\
                }, status=status.HTTP_200_OK)



