from django.urls import path
from . import views


urlpatterns = [
    path("", views.TweetsView.as_view()),
    path("<int:id>", views.TweetsView.as_view()),
    path("create", views.CreateTweetsView.as_view()),
    path("delete/<int:tweet_id>", views.DeleteTweetsView.as_view()),
    path("most_retweeted_tweets/", views.MostRetweetedTweetsView.as_view()),
    path("most_retweeted_tweets/<int:peopleId>", views.MostRetweetedTweetsByPeopleIdView.as_view()),
]