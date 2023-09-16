from django.urls import path, include
from medias import views

urlpatterns = [
    path("", views.MediasView.as_view()),
    path("type/<int:MediaType>", views.MediasView.as_view()),
    path("type/<int:MediaType>/<int:OrderBy>", views.MediasView.as_view()),
    path("<int:MediaId>", views.MediasView.as_view()),
    path("update_submedia", views.SubMediasUpdateView.as_view()),
    path("name", views.GetMediaByNameView.as_view()),
    path("people/<int:peopleId>/<int:MediaType>", views.GetMediaByPeopleIdView.as_view()),
    path("create", views.CreateMediasView.as_view()),
    path("delete/<int:media_id>", views.DeleteMediasView.as_view()),
    path("create_submedia", views.CreateSubMediasView.as_view()),
    path("delete_submedia/<int:submedia_id>", views.DeleteSubMediasView.as_view()),
    path("submedia/<int:MediaType>/<int:OrderBy>", views.SubMediasAPIView.as_view()),
    path("create_submedia_tag", views.CreateSubMediasTagsView.as_view()),
    path("delete_submedia_tag/<int:tag_id>", views.DeleteSubMediasTagsView.as_view()),
]

