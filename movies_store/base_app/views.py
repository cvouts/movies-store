from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Movie, User, RentMovie
from .serializers import MovieSerializer, RentMovieSerializer
from datetime import date

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

        if request.query_params.get("rating"):
            movies = movies.filter(rating=request.query_params.__getitem__("rating"))

        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"status": "401 Unauthorized",
                            "data": "You are not authorized to perform this action"},
                            status=status.HTTP_401_UNAUTHORIZED)

        if not request.user.is_staff:
            return Response({"status": "403 Forbidden",
                            "data": "You are not authorized to perform this action"},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def patch(self, request, id=None):
        if not request.user.is_authenticated:
            return Response({"status": "401 Unauthorized",
                            "data": "You are not authorized to perform this action"},
                            status=status.HTTP_401_UNAUTHORIZED)

        if not request.user.is_staff:
            return Response({"status": "403 Forbidden",
                            "data": "You are not authorized to perform this action"},
                            status=status.HTTP_403_FORBIDDEN)

        movie = Movie.objects.get(id=id)
        serializer = MovieSerializer(movie, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id=None):
        if not request.user.is_authenticated:
            return Response({"status": "401 Unauthorized",
                            "data": "You are not authorized to perform this action"},
                            status=status.HTTP_401_UNAUTHORIZED)

        if not request.user.is_staff:
            return Response({"status": "403 Forbidden",
                            "data": "You are not authorized to perform this action"},
                            status=status.HTTP_403_FORBIDDEN)

        movie = get_object_or_404(Movie, id=id)
        movie.delete()
        return Response({"status": "success", "data": "Movie Deleted"}, status=status.HTTP_202_ACCEPTED)


class RentMovieView(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"status": "401 Unauthorized",
                            "data": "You are not authorized to perform this action"},
                            status=status.HTTP_401_UNAUTHORIZED)

        serializer = RentMovieSerializer(data=request.data, partial=True)


        if not serializer.is_valid():
            get_object_or_404(Movie, id=request.data["movie"])
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
            get_object_or_404(Movie, id=request.data["movie"])
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        rentmovies = RentMovie.objects.filter(user=request.user,
                                              movie=serializer.validated_data["movie"],
                                              status="rented_currently")
        if len(rentmovies) == 1:

            this_rent = RentMovie.objects.get(user=request.user,
                                              movie=serializer.validated_data["movie"],
                                              status="rented_currently")
            cost = calculate_cost(this_rent.rent_date, date.today())
            this_rent.status = "rented_previously"
            this_rent.cost = cost
            this_rent.updated_date = date.today()
            this_rent.save()

            if cost < 0:
                return Response({"status": "400 Bad Request",
                                "data": ""},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({"status": "202 ACCEPTED",
                        "data": f"Movie returned successfully. You have been charged {cost} €"},
                        status=status.HTTP_202_ACCEPTED)
        else:
            return Response({"status": "400 Bad Request",
                            "data": "Movie is not currently rented"},
                            status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({"status": "401 Unauthorized",
                            "data": "You are not authorized to perform this action"},
                            status=status.HTTP_401_UNAUTHORIZED)
        #rented_list = RentMovie.objects.filter(user=request.user, status="rented_currently")

        rented_list = RentMovie.objects.filter(user=request.user)
        return_dict = {}
        i = 0
        for item in rented_list:
            if request.query_params.get("category") and item.movie.category != request.query_params.__getitem__("category"):
                continue

            if request.query_params.get("status") and item.status != request.query_params.__getitem__("status"):
                continue

            if request.query_params.get("rating") and item.movie.rating != float(request.query_params.__getitem__("rating")):
                continue

            key = f"#{i}"
            this_dict = {}
            this_dict["movie"] = item.movie.title
            this_dict["rented on"] = item.rent_date.strftime("%-d %B %Y")
            if item.status == "rented_currently":
                this_dict["cost"] = calculate_cost(item.rent_date, date.today())
                this_dict["returned on"] = "-"
                this_dict["status"] = "rented currently"
            else:
                this_dict["cost"] = calculate_cost(item.rent_date, item.updated_date)
                this_dict["returned on"] = item.updated_date.strftime("%-d %B %Y")
                this_dict["status"] = "rented previously"

            return_dict[key] = this_dict
            i += 1
        return Response(return_dict, status=status.HTTP_200_OK)


def calculate_cost(rent_date, return_or_current_date):
    time_passed = return_or_current_date - rent_date
    days_passed = time_passed.days
    if days_passed < 3:
        cost = days_passed + 1
    else:
        cost = 3 + (days_passed-2) * 0.5
    return cost
