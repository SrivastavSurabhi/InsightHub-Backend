import concurrent.futures

import pinecone
from django.utils.decorators import method_decorator
from django.views.decorators.vary import vary_on_headers
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from sentence_transformers import SentenceTransformer

from InsightHubAPI.constant import MediaType
from core.models import Genres
from medias.serializers import *
from .serializers import *

PINECONE_API_KEY = "3c5f3319-ea51-4973-8994-2528d9dcc91c"
PINECONE_ENVIRONMENT = "us-west1-gcp"
MODEL_NAME = "multi-qa-mpnet-base-dot-v1"
INDEX_NAME = "youtube-search"

class Pinecone:
    __doc__ = """For get pinecone"""
    authentication_classes = [JWTAuthentication]
    pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)

    def search_pinecone_index(query):
        xq = SentenceTransformer(MODEL_NAME).encode(query).tolist()
        res = pinecone.Index(INDEX_NAME).query(xq, top_k=5, include_metadata=True)
        matches = []
        for match in res['matches']:
            matches.append(match)

        pinecone_results = []
        for match in matches:
            original_text = str(match["metadata"]["text"])
            final_text = original_text.replace("[","" ).replace("]","" ).replace("'","" ).replace('"',"")
            pinecone_results.append({
                "text": final_text,
                "start": match["metadata"]["start"],
                "end": match["metadata"]["end"],
                "video_id": match["metadata"]["video_id"],
                "score": match["score"],
                "likesCount": match["metadata"]["likesCount"],
                "dislikesCount": match["metadata"]["dislikesCount"],
                "commentsCount": match["metadata"]["commentsCount"],
                "viewsCount": match["metadata"]["viewsCount"],
                "subMediaId": match["metadata"]["subMediaId"],
                "name": match["metadata"]["name"],
                "description": match["metadata"]["description"],
                "imagePath": match["metadata"]["imagePath"],
                "fileUrl": match["metadata"]["fileUrl"],
                "peopleId": match["metadata"]["peopleId"],
                "peopleName": match["metadata"]["peopleName"],
                "profileImagePath": match["metadata"]["profileImagePath"],
            })
        return pinecone_results

# create view class for semantic search
class SemanticSearchView(APIView):
    # Define a function to search the Pinecone index
    def search_pinecone(self, query):
        pinecone_results = Pinecone.search_pinecone_index(query)
        semantic_serializer = SemanticSearchSerializer(pinecone_results, many=True)
        return semantic_serializer

    # Define a function to filter SubMedias objects
    def search_submedias(self, query, mediaType=MediaType['Video']):
        submedias_results = SubMedias.objects.filter(name__icontains=query, medias__mediaType = mediaType,
                                                     publishedOn__isnull=False,isDeleted=False)[:10]
        submedia_serializer = SearchSubMediaSerializer(submedias_results, many=True)
        return submedia_serializer

    def search_submedias_tags(self, tag_name, people_id=None):
        if people_id:
            submedias_queryset = SubMedias.objects.filter(medias__people = people_id, medias__mediaType = MediaType['Video'],
                                                          publishedOn__isnull=False, isDeleted=False)
        else:
            submedias_queryset = SubMedias.objects.filter(medias__mediaType = MediaType['Video'],
                                                      publishedOn__isnull=False, isDeleted=False)

        submedia_ids = [submedia.subMediaId for submedia in submedias_queryset]
        submedias = SubMediasTags.objects.filter(subMediaId__in=submedia_ids, isDeleted=False, tagName = tag_name)[:10]
        submedia_records = [submedia.subMediaId for submedia in submedias]
        submedia_serializer = SubMediaSerializer(submedia_records, many=True)
        return submedia_serializer

    def get_people_based_on_query(self, query):
        people_results = Peoples.objects.filter(name__icontains=query, isDeleted=False)[:10]
        return people_results

    def get_people_based_on_genre(self, query):
        people_list = []
        try:
            # Filter Peoples objects based on query
            genreId = Genres.objects.get(name__iexact=query, isDeleted=False).genreId

            people_genres = PeopleGenreMapping.objects.filter(genreId=genreId)
            people_list = Peoples.objects.filter(peopleId__in=people_genres.values('peopleId'), isDeleted=False)

        except Genres.DoesNotExist:
            genre = None
        return people_list

    # Define a function to filter Peoples objects
    def search_peoples(self, query, executor):
        people1_future = executor.submit(self.get_people_based_on_query, query)
        people2_future = executor.submit(self.get_people_based_on_genre, query)

        people1_results = people1_future.result()
        people2_list = people2_future.result()

        # Merge peoples_results and people_genre
        peoples_results = list(set(people1_results) | set(people2_list))
        people_serializer = PeopleSerializer(peoples_results, many=True)
        return people_serializer

    @method_decorator(vary_on_headers("Authorization"))
    def get(self, request, *args, **kwargs):
        # if query is present in the request, then it takes precedence over tag and peopleId
        try:
            query = request.GET.get('query')
        except:
            query = None
        try:
            tag = request.GET.get('tag')
        except:
            tag = None
        try:
            peopleId = request.GET.get('peopleId')
        except:
            peopleId = 0

        # Create a ThreadPoolExecutor with a maximum of 3 worker threads
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=7)

        # Submit task for tag search if query is None
        if query is None:
            if tag is not None and peopleId != 0:
                executor.submit(self.search_submedias, query)
                submedias_by_tags = self.search_submedias_tags(tag, peopleId)
                return Response({"search_submedia": submedias_by_tags.data}, status=status.HTTP_200_OK)

        # Submit the tasks to the executor
        submedias_videos_future = executor.submit(self.search_submedias, query, MediaType['Video'])
        submedias_podcasts_future = executor.submit(self.search_submedias, query, MediaType['Podcast'])
        peoples_future = executor.submit(self.search_peoples, query, executor)
        submedia_videos_by_tags_future = executor.submit(self.search_submedias_tags, query)

        # Wait for all the futures to complete and retrieve their video_results
        submedias_videos_results = submedias_videos_future.result()
        submedias_podcasts_results = submedias_podcasts_future.result()
        peoples_results = peoples_future.result()
        submedia_videos_by_tags_results = submedia_videos_by_tags_future.result()

        # ## Add tags based submedias to title based submedias
        # Create a dictionary to store submedia data with subMediaId as the key
        submedia_videos_dict = {}
        for submedia in submedias_videos_results.data:
            submedia_videos_dict[submedia['subMediaId']] = submedia

        # Loop through submedia_videos_by_tags_results and add any submedia that is not already in the dictionary
        for submedia in submedia_videos_by_tags_results.data:
            if submedia['subMediaId'] not in submedia_videos_dict:
                submedia_videos_dict[submedia['subMediaId']] = submedia

        # Convert the dictionary back into a list of submedia data
        video_results = list(submedia_videos_dict.values())

        return Response({"search_submedia_videos": video_results,
                         "search_submedia_podcasts": submedias_podcasts_results.data,
                         "search_people": peoples_results.data}, status=status.HTTP_200_OK)
