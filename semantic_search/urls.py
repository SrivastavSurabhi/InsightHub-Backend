from django.urls import path
from . import views

#create URLS for semantic search
urlpatterns = [
    path("", views.SemanticSearchView.as_view()),
]