#create apps.py file
from django.apps import AppConfig

class SemanticSearchConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'semantic_search'
