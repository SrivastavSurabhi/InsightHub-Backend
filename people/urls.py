from django.urls import path, include
from . import views


urlpatterns = [
    path("", views.PeoplesView.as_view()),
    path("<int:id>", views.PeoplesView.as_view()),
    path("featured_people",views.GetFeaturedPeopleView.as_view()),
    path("get_latest_media_by_people/<int:peopleId>/<int:mediaType>",views.GetLatestMediaByPeopleView.as_view()),
    path("get_latest_media_by_people/<int:peopleId>/<int:mediaType>/<int:OrderBy>",views.GetLatestMediaByPeopleView.as_view()),
    path("get_popular_tags_by_people/<int:peopleId>",views.GetMostPopularTagsByPeopleView.as_view()),
    path("get_tweets_by_people/<int:peopleId>",views.GetTweetsByPeopleView.as_view()),
    path("create",views.CreatePeopleView.as_view()),
    path("delete/<int:people_id>",views.DeletePeopleView.as_view()),
    path("get_related_people/<int:people_id>",views.GetRelatedPeople.as_view()),
    path("get_people_by_static_ids",views.GetPeopleByStaticIdsView.as_view())
]
