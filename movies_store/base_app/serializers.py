from rest_framework import serializers
from .models import Movie, RentMovie
from django.urls import reverse

class MovieDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'title', 'category', 'details','rating']

class MovieBriefSerializer(serializers.ModelSerializer):
    details_url = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = ['title', 'category','rating', 'details_url']

    def get_details_url(self, obj):
        return reverse("movie_details", kwargs={"id" : obj.id})


class RentMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentMovie
        fields = ['user', 'movie', 'status', 'rent_date', 'updated_date', 'cost']
