from rest_framework import serializers
from .models import Movie, Comment


class MovieSerializer(serializers.ModelSerializer):
    allow_null = True

    class Meta:
        model = Movie
        fields = ['title', 'year', 'plot', 'language', 'country']


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ['text', 'movie']


class CommentTopSerializer(serializers.ModelSerializer):

    total_comments = serializers.IntegerField(read_only=True)
    rank = serializers.IntegerField(read_only=True)

    class Meta:
        model = Comment
        fields = ['movie', 'total_comments', 'rank']
