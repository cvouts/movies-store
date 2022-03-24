from rest_framework import serializers
from .models import Movie, User

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'title', 'category', 'details']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['movies_rented']
