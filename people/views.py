from collections import OrderedDict

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Count

from InsightHubAPI.common_import import *
from medias.serializers import *
from tweets.serializers import *


class PeoplesView(APIView,LimitOffsetPagination):
    __doc__ = """ Get All People or Particular People Info"""
    permission_classes = [HasAPIKey]
    pagination_class = LimitOffsetPagination

    def get_all_people(self):
        return Peoples.objects.filter(isDeleted=False)

    def get_people_by_id(self, id):
        try:
            return Peoples.objects.get(peopleId=id, isDeleted=False)
        except Peoples.DoesNotExist:
            raise Http404

    @method_decorator(cache_page(60*60*2))
    @method_decorator(vary_on_headers("Authorization"))
    def get(self, request, *args, **kwargs):
        latest_submedia_serializer = None
        try:
            people_id = int(kwargs['id'])
        except:
            people_id = 0

        if people_id > 0:
            people = self.get_people_by_id(people_id)
            serializer = PeopleDetailSerializer(people, many=False)
            last_submedia = SubMedias.objects.filter(medias__people = people.peopleId, medias__mediaType = MediaType['Video'], isDeleted=False).last()
            if last_submedia != None:
                latest_submedia_serializer = FeaturedMediaSerializer(last_submedia, many=False)
            return Response({"data":{"people":serializer.data,"latest_submedia":latest_submedia_serializer.data if latest_submedia_serializer != None else None}}, status=status.HTTP_200_OK)
        else :
            people = self.get_all_people()
            paginate_result = self.paginate_queryset(people, request, view=self)
            if paginate_result is not None:
                serializer =  PeopleSerializer(paginate_result, many=True)   
                return Response(OrderedDict([('count', self.count),('data', serializer.data)]))
            else:
                serializer = PeopleSerializer(people, many=True) 
                return Response({"count":people.count(),"data": serializer.data}, status=status.HTTP_200_OK)


class GetFeaturedPeopleView(APIView):
    __doc__ = """ Get featured people"""
    permission_classes = [HasAPIKey]
    pagination_class = pagination_settings.DEFAULT_PAGINATION_CLASS

    @method_decorator(cache_page(60*60*2))
    @method_decorator(vary_on_headers("Authorization"))
    def get(self, request, *args, **kwargs):
        people = Peoples.objects.filter(isFeatured=True, isDeleted=False).last()
        peopleserializer = PeopleDetailSerializer(people, many=False)
        peoplemedia = MediaPeopleMapping.objects.filter(peopleId=people,mediaId__mediaType = MediaType['Video']).last()
        submediaserializer = {}
        if peoplemedia != None:
            submedia = SubMedias.objects.filter(medias=peoplemedia.mediaId).last()
            if submedia != None:
                submediaserializer = FeaturedMediaSerializer(submedia, many=False).data
        return Response({"data":{"featured_people":peopleserializer.data,"featured_submedia":submediaserializer}}, status=status.HTTP_200_OK)


class GetLatestMediaByPeopleView(APIView,LimitOffsetPagination):
    __doc__ = """ Get latest medias by people """
    permission_classes = [HasAPIKey]
    pagination_class = LimitOffsetPagination

    def add_tags(self, serializer):
        submedia_ids = [submedia['subMediaId'] for submedia in serializer.data]
        tags = SubMediasTags.objects.filter(subMediaId__in=submedia_ids, isDeleted=False)
        tag_serializer = SubMediaTagSerializer(tags, many=True)
        for submedia in serializer.data:
            submedia_tags = []
            for tag in tag_serializer.data:
                if tag['subMediaId'] == submedia['subMediaId']:
                    submedia_tags.append(tag['tagName'])
            submedia['tags'] = submedia_tags
    
    @method_decorator(cache_page(60*60*2))
    @method_decorator(vary_on_headers("Authorization"))
    def get(self, request, *args, **kwargs):
        try:
            order_by = int(kwargs['OrderBy'])
        except:
            order_by = 0
        people_id = int(kwargs['peopleId'])
        media_type = int(kwargs['mediaType'])
        people = Peoples.objects.get(peopleId = people_id, isDeleted=False)
        peopleserializer = PeopleSerializer(people, many=False)
        submedias_queryset = SubMedias.objects.filter(medias__people = people.peopleId, medias__mediaType = media_type,
                                                      publishedOn__isnull=False, isDeleted=False)
        if order_by == OrderBy['ViewsCount']:
            latest_medias = submedias_queryset.order_by('-viewsCount')
        else:
            latest_medias = submedias_queryset.order_by('-publishedOn')
        paginate_result = self.paginate_queryset(latest_medias, request, view=self)
        if paginate_result is not None:
            latest_media_serializer = SubMediaSerializer(paginate_result, many=True)
            self.add_tags(latest_media_serializer)
            return Response(OrderedDict([('count', self.count),('data', {"people":peopleserializer.data,
                                                                         "latest_medias":latest_media_serializer.data})]))
        else:
            latest_media_serializer = SubMediaSerializer(latest_medias, many=True)
            self.add_tags(latest_media_serializer)
            return Response({"count":latest_medias.count(),"data": {"people":peopleserializer.data,
                                                                    "latest_medias":latest_media_serializer.data}},
                            status=status.HTTP_200_OK)

class GetMostPopularTagsByPeopleView(APIView,LimitOffsetPagination):
    __doc__ = """ Get latest tags by people """
    permission_classes = [HasAPIKey]
    pagination_class = LimitOffsetPagination

    @method_decorator(cache_page(60*60*2))
    @method_decorator(vary_on_headers("Authorization"))
    def get(self, request, *args, **kwargs):
        people_id = int(kwargs['peopleId'])
        people = Peoples.objects.get(peopleId = people_id, isDeleted=False)
        peopleserializer = PeopleSerializer(people, many=False)
        submedias_queryset = SubMedias.objects.filter(medias__people = people.peopleId, medias__mediaType = MediaType['Video'],
                                                      publishedOn__isnull=False, isDeleted=False)

        try:
            limit = int(request.GET.get('limit', 10))
            offset = int(request.GET.get('offset', 0))
        except ValueError:
            return Response({'error': 'Invalid limit/offset value'}, status=status.HTTP_400_BAD_REQUEST)

        submedia_ids = [submedia.subMediaId for submedia in submedias_queryset]
        popular_tags = SubMediasTags.objects.filter(subMediaId__in=submedia_ids, isDeleted=False)\
            .values('tagName')\
            .annotate(tagCount=Count('tagName'))\
            .order_by('-tagCount')
        paginate_result = self.paginate_queryset(popular_tags, request, view=self)
        tag_serializer = SubMediaTagCountSerializer(paginate_result, many=True)
        return Response(OrderedDict([('count', self.count),('data', {"people":peopleserializer.data,
                                                            "latest_tags":tag_serializer.data})]))

class GetTweetsByPeopleView(APIView, LimitOffsetPagination):
    __doc__ = """ Get latest tweets by people"""
    permission_classes = [HasAPIKey]
    pagination_class = LimitOffsetPagination

    @method_decorator(cache_page(60*60*2))
    @method_decorator(vary_on_headers("Authorization"))
    def get(self, request, *args, **kwargs):
        people_id = int(kwargs['peopleId'])
        people = Peoples.objects.get(peopleId = people_id, isDeleted=False)
        latest_tweets = Tweets.objects.filter(tweetedByPersonId = people.peopleId, isDeleted=False).distinct().order_by("-tweetId")
        paginate_results = self.paginate_queryset(latest_tweets, request, view=self)
        if paginate_results is not None:
            serializer =  TweetsSerializer(paginate_results, many=True)   
            return Response(OrderedDict([('count', self.count),('data', serializer.data)]))
        else:
            serializer = TweetsSerializer(latest_tweets, many=True) 
            return Response({"count":latest_tweets.count(),"data": serializer.data}, status=status.HTTP_200_OK)


class CreatePeopleView(APIView):
    __doc__ = """For add new people"""
    serializer_class = PeopleCreateSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]
    pagination_class = pagination_settings.DEFAULT_PAGINATION_CLASS

    def post(self, request, *args, **kwargs):
        data = request.data
        user = request.user.id
        data['createdBy'] = data['modifiedBy']= user
        serializer = self.serializer_class(data=data)
        return commonPostApi(serializer)


class DeletePeopleView(APIView):
    __doc__ = """For delete people"""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsAdminUser]

    def delete(self, request, people_id, *args, **kwargs):
        return commonDeleteApi(Peoples, people_id)


class GetRelatedPeople(APIView,LimitOffsetPagination):
    __doc__ = """Get Related People on the basis of peopleId."""
    permission_classes = [HasAPIKey]
    pagination_class = LimitOffsetPagination

    @method_decorator(cache_page(60*60*2))
    @method_decorator(vary_on_headers("Authorization"))
    def get(self, request, *args, **kwargs):
        people_id = int(kwargs['people_id'])
        peoplegnere = PeopleGenreMapping.objects.filter(peopleId = people_id).values('genreId')
        peoples = Peoples.objects.filter(peoplegenremapping__genreId__in = peoplegnere)\
            .distinct().exclude(peoplegenremapping__peopleId=people_id)
        paginate_result = self.paginate_queryset(peoples, request, view=self)
        if paginate_result is not None:
            serializer =  PeopleSerializer(paginate_result, many=True)   
            return Response(OrderedDict([('count', self.count),('data', serializer.data)]))
        else:
            serializer = PeopleSerializer(peoples, many=True) 
            return Response({"count":peoples.count(),"data": serializer.data}, status=status.HTTP_200_OK)

class GetPeopleByStaticIdsView(APIView):
    __doc__ = """ Get people by static ids """
    permission_classes = [HasAPIKey]
    @method_decorator(cache_page(60*60*2))
    @method_decorator(vary_on_headers("Authorization"))
    def get(self, request, *args, **kwargs):
        people_ids = ['14', '22', '26', '35', '53', '76', '30', '33', '54', '62', '21', '68', '71', '72', '73', '90', '100', '34', '36', '13', '52', '83', '28', '56', '64', '77', '94', '31', '85', '74']
        # Deduplicate the list
        people_ids = list(set(people_ids))
        people_ids = [int(people_id) for people_id in people_ids]
        people = Peoples.objects.filter(peopleId__in=people_ids, isDeleted=False)
        serializer = PeopleSerializer(people, many=True)
        return Response({"count":people.count(),"data": serializer.data}, status=status.HTTP_200_OK)