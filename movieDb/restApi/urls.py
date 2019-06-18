from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views, api

urlpatterns = [
    path('movies', api.Movies.as_view()),
    path('comments', api.Comments.as_view()),
    path('top', api.Top.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)