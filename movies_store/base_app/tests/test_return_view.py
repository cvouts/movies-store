from django.test import TestCase
from django.urls import reverse
from base_app.models import Movie, RentMovie, User
from rest_framework.test import APIClient
from datetime import date, timedelta
from base_app.views import calculate_cost

class RentViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Movie.objects.create(title="Lord of the Rings", category="Fantasy",
                             rating=9)
        Movie.objects.create(title="Matrix", category="Sci-Fi",
                             rating=7)
        User.objects.create_user(username="user", password="password")

        movie = Movie.objects.get(id=1)
        user = User.objects.get(id=1)

        RentMovie.objects.create(user=user, movie=movie,
                                 status=RentMovie.RentStatus.CURRENT)


    def test_other_methods(self):
        response = self.client.get(reverse("return"), {"movie" : "1"})
        self.assertEqual(response.status_code, 405)

        response = self.client.patch(reverse("return"), {"movie" : "1"})
        self.assertEqual(response.status_code, 405)

        response = self.client.delete(reverse("return"), {"movie" : "1"})
        self.assertEqual(response.status_code, 405)

    def test_not_logged_in(self):
        response = self.client.post(reverse("return"), {"movie" : "1"})
        self.assertEqual(response.status_code, 401)

    def login(self):
        client = APIClient()
        user = User.objects.get(username="user")
        client.force_authenticate(user=user)
        return client

    def test_return_404(self):
        client = self.login()
        response = client.post(reverse("return"), {"movie" : "1221"})
        self.assertEqual(response.status_code, 404)

    def test_return_202_then_400(self):
        client = self.login()
        user = User.objects.get(username="user")

        rentals = RentMovie.objects.filter(user=user,
                            movie=Movie.objects.get(id=1),
                            status="rented currently")
        self.assertEqual(len(rentals), 1)
        response = client.post(reverse("return"), {"movie" : "1"})

        self.assertEqual(response.status_code, 202)
        rentals = RentMovie.objects.filter(user=user,
                            movie=Movie.objects.get(id=1),
                            status="rented currently")
        self.assertEqual(len(rentals), 0)

        response = client.post(reverse("return"), {"movie" : "1"})
        self.assertEqual(response.status_code, 400)

    def test_cost(self):
        today = date.today()
        cost = calculate_cost(today - timedelta(days=0), today)
        self.assertEqual(cost, 1.0)
        cost = calculate_cost(today - timedelta(days=1), today)
        self.assertEqual(cost, 2.0)
        cost = calculate_cost(today - timedelta(days=2), today)
        self.assertEqual(cost, 3.0)
        cost = calculate_cost(today - timedelta(days=3), today)
        self.assertEqual(cost, 3.5)
        cost = calculate_cost(today - timedelta(days=4), today)
        self.assertEqual(cost, 4.0)
        cost = calculate_cost(today - timedelta(days=14), today)
        self.assertEqual(cost, 9.0)
        cost = calculate_cost(today - timedelta(days=400), today)
        self.assertEqual(cost, 202.0)

    def test_negative_cost(self):
        client = self.login()
        today = date.today()

        user = User.objects.get(id=1)
        movie = Movie.objects.get(id=1)
        movie_rent = RentMovie.objects.get(id=1)
        movie_rent.rent_date = today + timedelta(days=2)
        movie_rent.save()

        response = client.post(reverse("return"), {"movie" : "1"})
        rentals = RentMovie.objects.filter(user=user, movie=movie)
        for rental in rentals:
            movie_rent.cost = rental.cost
            movie_rent.save()
            self.assertEqual(response.status_code, 500)
