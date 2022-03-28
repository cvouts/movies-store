from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Movie, User, RentMovie
from .serializers import (MovieDetailsSerializer, MovieBriefSerializer,
RentMovieSerializer)
from datetime import date

# Create your views here.
class MoviesView(APIView):
    def get(self, request, id=None):
        if id:
            movie = get_object_or_404(Movie, id=id)
            serializer = MovieDetailsSerializer(movie)
            return Response(serializer.data, status=status.HTTP_200_OK)

        filters = {}
        if request.query_params.get("category"):
            filters["category"] = request.query_params.get("category")
        if request.query_params.get("rating"):
            filters["rating"] = request.query_params.get("rating")
        movies = Movie.objects.filter(**filters)
        serializer = MovieBriefSerializer(movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def check_authentication(self, request):
        if not request.user.is_authenticated:
            return Response({"status": "401 Unauthorized",
                            "data": "You are not authorized to perform this action"},
                            status=status.HTTP_401_UNAUTHORIZED)

        if not request.user.is_staff:
            return Response({"status": "403 Forbidden",
                            "data": "You are not authorized to perform this action"},
                            status=status.HTTP_403_FORBIDDEN)
        return None

    def post(self, request):
        authentication = self.check_authentication(request)
        if authentication != None:
            return authentication

        serializer = MovieDetailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id=None):
        authentication = self.check_authentication(request)
        if authentication != None:
            return authentication

        movie = get_object_or_404(Movie, id=id)
        serializer = MovieDetailsSerializer(movie, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id=None):
        authentication = self.check_authentication(request)
        if authentication != None:
            return authentication

        movie = get_object_or_404(Movie, id=id)
        movie.delete()
        return Response({"status": "success", "data": "Movie Deleted"},
                         status=status.HTTP_202_ACCEPTED)


class RentMovieView(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"status": "401 Unauthorized",
                            "data": "You are not authorized to perform this action"},
                            status=status.HTTP_401_UNAUTHORIZED)

        serializer = RentMovieSerializer(data=request.data, partial=True)

        if not serializer.is_valid():
            if serializer.errors["movie"][0].code == "does_not_exist":
                return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        rent_entries_count = RentMovie.objects.filter(user=request.user,
                                              movie=serializer.validated_data["movie"],
                                              status="rented_currently").count()

        if rent_entries_count == 0:
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
            if serializer.errors["movie"][0].code == "does_not_exist":
                return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        rent_entries = RentMovie.objects.filter(user=request.user,
                                              movie=serializer.validated_data["movie"],
                                              status="rented_currently")
        if len(rent_entries) == 1:
            this_rent = rent_entries[0]

            cost = calculate_cost(this_rent.rent_date, date.today())
            this_rent.status = RentMovie.RentStatus.PREVIOUS
            this_rent.cost = cost
            this_rent.updated_date = date.today()
            this_rent.save()

            if cost <= 0:
                return Response({"status": "500 Internal Server Error",
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

        filters = {"user" : request.user}
        if request.query_params.get("status"):
            filters["status"] = request.query_params.get("status")
        if request.query_params.get("title"):
            filters["movie__title"] = request.query_params.get("title")
        if request.query_params.get("category"):
            filters["movie__category"] = request.query_params.get("category")
        if request.query_params.get("rating"):
            filters["movie__rating"] = request.query_params.get("rating")
        rented_list = RentMovie.objects.filter(**filters)

        return_dict = {}
        i = 1
        for item in rented_list:
            key = f"#{i}"
            this_dict = {}
            this_dict["movie"] = item.movie.title
            this_dict["rented on"] = item.rent_date.strftime("%-d %B %Y")
            if item.status == RentMovie.RentStatus.CURRENT:
                this_dict["cost"] = calculate_cost(item.rent_date, date.today())
                this_dict["returned on"] = "-"
                this_dict["status"] = "rented_currently"
            else:
                this_dict["cost"] = item.cost
                this_dict["returned on"] = item.updated_date.strftime("%-d %B %Y")
                this_dict["status"] = "rented_previously"

            return_dict[key] = this_dict
            i += 1
        return Response(return_dict, status=status.HTTP_200_OK)


def calculate_cost(rent_date, return_or_current_date):
    time_passed = return_or_current_date - rent_date
    days_passed = time_passed.days

    if days_passed < 3:
        # the cost on the first day (days_passed==0) is 1. Therefore if
        # days_passed is 0, 1, or 2, the cost is 1, 2 or 3 respectively.
        cost = days_passed + 1
    else:
        # if days_passed > 2, we know the cost is at least 3. We then add 0.5
        # to the cost, for every additional day after the third.
        cost = 3 + (days_passed-2) * 0.5
    return cost
