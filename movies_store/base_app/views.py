from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Movie, User, RentMovie
from .serializers import MovieSerializer, RentMovieSerializer
from datetime import datetime

# Create your views here.
class MoviesView(APIView):

    def get(self, request, id=None):
        if id:
            movie = Movie.objects.get(id=id)
            serializer = MovieSerializer(movie)
            return Response(serializer.data, status=status.HTTP_200_OK)

        movies = Movie.objects.all()
        if request.query_params.get("category"):
            movies = movies.filter(category=request.query_params.__getitem__("category"))

        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if request.user.is_staff:
            print(request.data)
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


class RentMovieView(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"status": "401 Unauthorized",
                            "data": "You are not authorized to perform this action"},
                            status=status.HTTP_401_UNAUTHORIZED)

        serializer = RentMovieSerializer(data=request.data, partial=True)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        rentmovies = RentMovie.objects.filter(user=request.user,
                                              movie=serializer.validated_data["movie"]).exclude(status="rented_previously")
        if len(rentmovies) == 0:
            serializer.save(user=request.user, status="rented_currently")
            return Response({"status": "202 ACCEPTED",
                        "data": "Movie rented successfully"},
                        status=status.HTTP_202_ACCEPTED)
        else:
            return Response({"status": "400 Bad Request",
                            "data": "Movie has already been rented"},
                            status=status.HTTP_400_BAD_REQUEST)


class ReturnMovieView(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"status": "401 Unauthorized",
                            "data": "You are not authorized to perform this action"},
                            status=status.HTTP_401_UNAUTHORIZED)

        serializer = RentMovieSerializer(data=request.data, partial=True)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        rentmovies = RentMovie.objects.filter(user=request.user,
                                              movie=serializer.validated_data["movie"],
                                              status="rented_currently")
        if len(rentmovies) == 1:

            this_rent = RentMovie.objects.get(user=request.user,
                                              movie=serializer.validated_data["movie"],
                                              status="rented_currently")
            cost = this_rent.get_cost()

            rentmovies.update(status="rented_previously", cost=cost)
            return Response({"status": "202 ACCEPTED",
                        "data": f"Movie returned successfully. You have been charged {cost} €"},
                        status=status.HTTP_202_ACCEPTED)
        else:
            return Response({"status": "400 Bad Request",
                            "data": "Movie is not currently rented"},
                            status=status.HTTP_400_BAD_REQUEST)
