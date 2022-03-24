from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Movie, User
from .serializers import MovieSerializer, UserSerializer

# Create your views here.
class MoviesView(APIView):

    def get(self, request, id=None, category=None):
        if id:
            movie = Movie.objects.get(id=id)
            serializer = MovieSerializer(movie)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif category:
            movies = Movie.objects.filter(category=category)
            serializer = MovieSerializer(movies, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):

        if request.user.is_staff:
            serializer = MovieSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"status": "401 Unauthorized",
                            "data": "You are not authorized to perform this action"},
                            status=status.HTTP_401_UNAUTHORIZED)

    def patch(self, request, id=None):
        if request.user.is_staff:
            movie = Movie.objects.get(id=id)
            serializer = MovieSerializer(movie, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"status": "401 Unauthorized",
                            "data": "You are not authorized to perform this action"},
                            status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, id=None):
        if request.user.is_staff:
            movie = get_object_or_404(Movie, id=id)
            movie.delete()
            return Response({"status": "success", "data": "Movie Deleted"})
        else:
            return Response({"status": "401 Unauthorized",
                            "data": "You are not authorized to perform this action"},
                            status=status.HTTP_401_UNAUTHORIZED)


class RentView(APIView):

    def get(self, request, id):
        if request.user.is_authenticated:
            movie = Movie.objects.get(id=id)
            this_user = User.objects.get(id=request.user.id)
            this_user.movies_rented.add(movie)
            serializer = UserSerializer(this_user)
            return Response(serializer.data, status=status.HTTP_200_OK)
