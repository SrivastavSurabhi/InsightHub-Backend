from django.urls import path, include
from . import views


urlpatterns = [
    path('login/', views.CustomTokenObtainPairView.as_view(), name='loginview'),
    path('get_api_key/', views.APITokenView.as_view(), name='apitokenview'),
    path("genre", views.GenreView.as_view()),
    path("genre/create", views.CreateGenreView.as_view()),
    path("genre/delete/<int:genre_id>", views.DeleteGenreView.as_view()),
    path("search/<str:Search>", views.SearchView.as_view()),
    path("search", views.SearchPostView.as_view()),
    path("get_data_by_genre/<int:genre_id>", views.GetDataByGenreIdView.as_view())

]