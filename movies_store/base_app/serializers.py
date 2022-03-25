from rest_framework import serializers
from .models import Movie, RentMovie

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'title', 'category', 'details']

class RentMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = RentMovie
        fields = ['user', 'movie', 'status', 'rent_date', 'updated_date', 'cost']
