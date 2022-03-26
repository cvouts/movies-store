from django.test import TestCase
from django.urls import reverse
from base_app.models import Movie, RentMovie, User
from rest_framework.test import APIClient
import datetime

class RentViewTest(TestCase):
    def setUp(self):
        self.movie_1 = Movie.objects.create(title="Lord of the Rings", category="Fantasy")
        movie_2 = Movie.objects.create(title="Matrix", category="Sci-Fi")
        movie_3 = Movie.objects.create(title="Narnia", category="Fantasy")
        self.movie_1.save()
        movie_2.save()
        movie_3.save()

        user = User.objects.create_user(username="user", password="password")
        user.save()

        self.movie_rent = RentMovie.objects.create(user=user, movie=self.movie_1, status="rented_currently")
        self.movie_rent.save()

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

    def test_return(self):
        client = APIClient()
        user = User.objects.get(username="user")
        client.force_authenticate(user=user)

        response = client.post(reverse("return"), {"movie" : "1221"})
        self.assertEqual(response.status_code, 404)

        rentals = RentMovie.objects.filter(user=user, movie=self.movie_1, status="rented_currently")
        self.assertEqual(len(rentals), 1)
        response = client.post(reverse("return"), {"movie" : "1"})
        self.assertEqual(response.status_code, 202)
        rentals = RentMovie.objects.filter(user=user, movie=self.movie_1, status="rented_currently")
        self.assertEqual(len(rentals), 0)

    def test_cost_wrapper(self):
        client = APIClient()
        user = User.objects.get(username="user")
        client.force_authenticate(user=user)

        today = datetime.date.today()
        self.cost_cases(today - datetime.timedelta(days=0), 1.0, client, user)
        self.cost_cases(today - datetime.timedelta(days=1), 2.0, client, user)
        self.cost_cases(today - datetime.timedelta(days=2), 3.0, client, user)
        self.cost_cases(today - datetime.timedelta(days=3), 3.5, client, user)
        self.cost_cases(today - datetime.timedelta(days=4), 4.0, client, user)
        self.cost_cases(today - datetime.timedelta(days=14), 9.0, client, user)
        self.cost_cases(today - datetime.timedelta(days=400), 202.0, client, user)
        self.cost_cases(today + datetime.timedelta(days=2), -3.0, client, user)

    def cost_cases(self, mock_rent_date, cost, client, user):
        self.movie_rent.rent_date = mock_rent_date
        self.movie_rent.save()
        response = client.post(reverse("return"), {"movie" : "1"})

        rentals = RentMovie.objects.filter(user=user, movie=self.movie_1)
        for rental in rentals:
            self.movie_rent.cost = rental.cost
            self.movie_rent.save()

            if self.movie_rent.cost < 0:
                self.assertEqual(response.status_code, 500)
            else:
                self.assertEqual(self.movie_rent.cost, cost)
        client.post(reverse("rent"), {"movie" : "1"})
