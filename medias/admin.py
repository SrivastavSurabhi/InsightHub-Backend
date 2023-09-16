from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Medias)
admin.site.register(SubMedias)
admin.site.register(SubMediasTags)
admin.site.register(MediaPeopleMapping)
admin.site.register(MediaGenreMapping)