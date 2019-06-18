import requests
import re
from django.db.models import Count
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Comment, Movie
from .serializers import CommentSerializer, MovieSerializer, CommentTopSerializer
from django.core import serializers

def set_if_not_none(mapping, key, value):
    if value is not None:
        mapping[key] = value

class Movies(APIView):

    '''
    example post data: {"title":"Avatar"}
    example url: /movies?language=English&year=1993
    example url: /movies?language=English&sort=year

    '''

    def get(self, request, format=None):
        filter_params = {}
        set_if_not_none(filter_params, 'year', request.GET.get('year'))
        set_if_not_none(filter_params, 'language', request.GET.get('language'))

        obj = Movie.objects.all().filter(**filter_params)

        if 'sort' in request.query_params:
            obj = obj.order_by(request.GET.get('sort'))
            
        serializer = MovieSerializer(obj, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        if(request.data.items().__len__() == 1 and 'title' in request.data):
            serializer = MovieSerializer(data=request.data)

            if serializer.is_valid():
                r = requests.get(
                    'http://www.omdbapi.com/?t={}&apikey=43ed7be1'.format(
                        request.data['title']
                    )
                )
                obj = r.json()

                serializer.save(
                    year=obj['Year'],
                    plot=obj['Plot'],
                    language=obj['Language'],
                    country=obj['Country']
                )

                return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class Comments(APIView):

    '''
    example post data: {"movie":"2", "text":"Lorem ipsum"}
    example url: /comments?movie=1

    '''

    def get(self, request, format=None):
        obj = Comment.objects.all()
        get_data = request.query_params

        if 'movie' in get_data:
            obj = obj.filter(movie=get_data['movie'])

        serializer = CommentSerializer(obj, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CommentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Top(APIView):
    '''
    example url: /top?from=2019-06-16&to=2019-06-19
    example url: /top?from=2019-06-18&to=2019-06-19

    '''

    def get(self, request, format=None):
        get_data = request.query_params
        if 'from' in get_data and 'to' in get_data:

            regDate = r"^[\d]{4}-[\d]{1,2}-[\d]{1,2}$"
            if re.match(regDate, get_data['from']) and re.match(regDate, get_data['to']):
                query = f"""
                    SELECT
                    id,
                    movie_id,
                    date,
                    DENSE_RANK () OVER ( ORDER BY count(movie_id) DESC) rank,
                    count(movie_id) as total_comments
                    FROM restApi_comment
                    WHERE date between '{get_data['from']}' and
                    '{get_data['to']}'
                    GROUP BY movie_id
                    ORDER BY -total_comments
                    """
                serializer = CommentTopSerializer(Comment.objects.raw(query), many=True)
                return Response(serializer.data)
            else:
                return Response("Bad date format", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Specify date range", status=status.HTTP_400_BAD_REQUEST)
