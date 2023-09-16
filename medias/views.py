import traceback

from .serializers import *
from InsightHubAPI.common_import import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from django.db.models import Prefetch
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.pagination import LimitOffsetPagination
from collections import OrderedDict
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie, vary_on_headers
from django.db.models import Count, Q


class MediasView(APIView,LimitOffsetPagination):
    __doc__ = "To get all medias and get media by id and get media by type."
    permission_classes = [HasAPIKey]
    pagination_class = pagination_settings.DEFAULT_PAGINATION_CLASS

    def get_all_media(self):
        return Medias.objects.filter(isDeleted = False)

    def get_media_by_id(self, id):
        try:
            return Medias.objects.get(mediaId=id,isDeleted = False)
        except Medias.DoesNotExist:
            raise Http404

    def get_media_by_type(self, media_type,order_by):
        submedias_queryset =SubMedias.objects.filter(isDeleted=False)
        medias_queryset = Medias.objects.filter(mediaType=media_type,isDeleted = False)
        try:  
            if order_by == OrderBy['ViewsCount']:
                return medias_queryset.prefetch_related(Prefetch('subMedias',\
                    queryset=submedias_queryset.order_by('-viewsCount')))
            else:
                return medias_queryset.prefetch_related(Prefetch('subMedias',\
                    queryset=submedias_queryset.order_by('-createdOnUtc')))
        except Medias.DoesNotExist:
            raise Http404

    @method_decorator(cache_page(60*60*2))
    @method_decorator(vary_on_headers("Authorization"))
    def get(self, request, *args, **kwargs):
        try:
            media_id = kwargs['MediaId']
        except:
            media_id = 0
        try:
            media_type = kwargs['MediaType'] 
        except:
            media_type = 0
        try:
            order_by = kwargs['OrderBy'] 
        except:
            order_by = 0
        if media_id > 0:
            medias = self.get_media_by_id(media_id)
            serializer = MediaDetailSerializer(medias, many=False)
            return Response({"data": serializer.data}, status=status.HTTP_200_OK)
        elif media_type > 0:
            medias = self.get_media_by_type(media_type,order_by)
            serializer = MediaDetailSerializer(medias, many=True)
        else:
            medias = self.get_all_media()
        results = self.paginate_queryset(medias, request, view=self)
        if results is not None:
            serializer =  MediaSerializer(results, many=True)   
            return Response(OrderedDict([('count', self.count),('data', serializer.data)]))
        else:
            serializer = MediaSerializer(medias, many=True) 
            return Response({"count":medias.count(),"data": serializer.data}, status=status.HTTP_200_OK)

class GetMediaByPeopleIdView(APIView):
    permission_classes = [HasAPIKey]
    def get_media_by_people(self, people_id, media_type):
        try:
            return Medias.objects.filter(mediaType=media_type, mediapeople__peopleId=people_id).first()
        except Medias.DoesNotExist:
            raise Http404

    def get(self, request, *args, **kwargs):
        try:
            people_id = kwargs['peopleId']
            media_type = kwargs['MediaType']
        except:
            raise Http404

        media = self.get_media_by_people(people_id, media_type)
        serializer =  MediaSpeificSerializer(media, many=False)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

class CreateMediasView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,IsAdminUser]
    pagination_class = pagination_settings.DEFAULT_PAGINATION_CLASS

    __doc__ = "To create medias"

    def post(self, request, *args, **kwargs):
        mediaChoice = [1, 2, 3]
        data = request.data
        user = request.user.id
        data['createdBy'] = data['modifiedBy']= user
        serializer = CreateMediaSerializer(data=data)
        try:
            mediaType = request.data['mediaType']
        except:
            mediaType = None
        if mediaType not in mediaChoice and mediaType != None:
            raise serializers.ValidationError({'mediaType':errors.MEDIATYPE}, code=status.HTTP_400_BAD_REQUEST)
        return commonPostApi(serializer)

class CreateSubMediasTagsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,IsAdminUser]
    def post(self, request):
        try:
            data = request.data
            user = request.user.id
            data['createdBy'] = data['modifiedBy']= user
            serializer = CreateSubMediaTagSerializer(data=data)
            return commonPostApi(serializer)
        except:
            traceback.print_exc()
            return None

class SubMediasAPIView(APIView, LimitOffsetPagination):
    permission_classes = [HasAPIKey]
    pagination_class = pagination_settings.DEFAULT_PAGINATION_CLASS

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

    def get(self, request, *args, **kwargs):
        try:
            media_type = kwargs['MediaType']
        except:
            media_type = 0

        try:
            order_by = kwargs['OrderBy']
        except:
            order_by = 0

        submedias = SubMedias.objects.filter(medias__mediaType=media_type, publishedOn__isnull=False, isDeleted=False)

        if media_type == 2:
            submedias = submedias.filter(viewsCount__gt=5000)

        if order_by == OrderBy['ViewsCount']:
            submedias = submedias.order_by('-viewsCount')
        else:
            submedias = submedias.order_by('-publishedOn')

        page = self.paginate_queryset(submedias, request, view=self)


        if page is not None:
            # get list of subMediaIds from the serializer data
            serializer = SubMediaSerializer(page, many=True)
            self.add_tags(serializer)
            return Response(OrderedDict([('count', self.count),('data', serializer.data)]))

        serializer = SubMediaSerializer(submedias, many=True)
        self.add_tags(serializer)
        return Response({"count":submedias.count(),"data": serializer.data}, status=status.HTTP_200_OK)


class CreateSubMediasView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,IsAdminUser]
    pagination_class = pagination_settings.DEFAULT_PAGINATION_CLASS

    __doc__ = "To create submedias"

    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            user = request.user.id
            data['createdBy'] = data['modifiedBy']= user
            serializer = CreateSubMediaSerializer(data=data)
            return commonPostApi(serializer)
        except:
            traceback.print_exc()
            return None


class DeleteMediasView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,IsAdminUser]

    __doc__ = "To delete medias"

    def delete(self, request, media_id, *args, **kwargs):
        return commonDeleteApi(Medias, media_id)


class DeleteSubMediasView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,IsAdminUser]

    __doc__ = "To delete submedias"

    def delete(self, request, submedia_id, *args, **kwargs):
        return commonDeleteApi(SubMedias, submedia_id)

class DeleteSubMediasTagsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,IsAdminUser]

    __doc__ = "To delete submedias tags"

    def delete(self, request, tag_id, *args, **kwargs):
        return commonDeleteApi(SubMediasTags, tag_id)

class SubMediasUpdateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,IsAdminUser]
    def put(self, request):
        try:
            sub_media_id = request.data.get('subMediaId')
            sub_media = SubMedias.objects.get(pk=sub_media_id)
        except SubMedias.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        published_date = request.data.get('publishedDate')
        if not published_date:
            return Response({'error': 'publishedDate is required'}, status=status.HTTP_400_BAD_REQUEST)

        sub_media.publishedOn = published_date
        sub_media.save()
        return Response({'success': 'SubMedia updated successfully'}, status=status.HTTP_200_OK)

class GetMediaByNameView(APIView):
    permission_classes = [HasAPIKey]
    def get_media_by_name(self, name, media_type):
        try:
            medias = Medias.objects.filter(
                Q(authorName=name) & Q(mediaType=media_type),
                isDeleted=False
            ).annotate(sub_media_count=Count('subMedias')).filter(sub_media_count__gt=0)

            medias = medias.order_by('-sub_media_count')
            return medias.first()
        except Medias.DoesNotExist:
            raise Http404
    def get(self, request, *args, **kwargs):
        try:
            media_name = request.data['name']
            media_type = request.data['mediaType']
        except:
            raise Http404

        media = self.get_media_by_name(media_name, media_type)
        serializer =  MediaSpeificSerializer(media, many=False)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)