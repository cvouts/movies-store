from django.test import TestCase
from django.urls import reverse
from base_app.models import Movie, RentMovie, User
from rest_framework.test import APIClient
from datetime import date, timedelta
from base_app.views import calculate_cost

class ProfileViewTest(TestCase):
    def setUp(self):
        movie_1 = Movie.objects.create(title="Lord of the Rings",
                                       category="Fantasy",
                                       rating=9)
        movie_2 = Movie.objects.create(title="Matrix",
                                       category="Sci-Fi",
                                       rating=7)
        movie_3 = Movie.objects.create(title="Narnia",
                                       category="Fantasy",
                                       rating=6)
        movie_4 = Movie.objects.create(title="Warcraft",
                                       category="Fantasy",
                                       rating=6)

        user = User.objects.create_user(username="user", password="password")

        RentMovie.objects.create(user=user, movie=movie_1,
                                 status="rented currently")
        RentMovie.objects.create(user=user, movie=movie_2,
                                 status=RentMovie.RentStatus.CURRENT)
        RentMovie.objects.create(user=user, movie=movie_4,
                                 status=RentMovie.RentStatus.PREVIOUS)

    def test_other_methods(self):
        response = self.client.post(reverse("profile"))
        self.assertEqual(response.status_code, 405)
        response = self.client.patch(reverse("profile"))
        self.assertEqual(response.status_code, 405)
        response = self.client.delete(reverse("profile"))
        self.assertEqual(response.status_code, 405)

    def test_not_logged_in(self):
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 401)

    def login(self):
        client = APIClient()
        user = User.objects.get(username="user")
        client.force_authenticate(user=user)
        return client

    def test_profile_simple(self):
        client = self.login()
        response = client.get(reverse("profile"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)

    def test_parameters_category(self):
        client = self.login()
        response = client.get(reverse("profile"), {"category": "Fantasy"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_parameters_category_not_valid(self):
        client = self.login()
        response = client.get(reverse("profile"), {"category": "not a category"})
        self.assertEqual(len(response.data), 0)

    def test_parameters_status_current(self):
        client = self.login()
        response = client.get(reverse("profile"), {"status": "rented currently"})
        self.assertEqual(len(response.data), 2)

    def test_parameters_status_previous(self):
        client = self.login()
        response = client.get(reverse("profile"), {"status": "rented previously"})
        self.assertEqual(len(response.data), 1)

    def test_parameters_status_not_valid(self):
        client = self.login()
        response = client.get(reverse("profile"), {"status": "not a status"})
        self.assertEqual(len(response.data), 0)

    def test_parameters_category_status(self):
        client = self.login()
        response = client.get(reverse("profile"),
                               {"status": "rented previously",
                                "category": "Fantasy"})
        self.assertEqual(len(response.data), 1)

    def test_parameters_rating(self):
        client = self.login()
        response = client.get(reverse("profile"), {"rating" : 9.0})
        self.assertEqual(len(response.data), 1)

    def test_costs(self):
        client = APIClient()
        user = User.objects.get(username="user")
        client.force_authenticate(user=user)
        today = date.today()

        movie_rent_1 = RentMovie.objects.get(id=1)
        movie_rent_1.rent_date = today - timedelta(days=3)
        movie_rent_1.save()

        movie_rent_2 = RentMovie.objects.get(id=2)
        movie_rent_2.rent_date = today - timedelta(days=6)
        movie_rent_2.save()

        movie_rent_3 = RentMovie.objects.get(id=3)
        movie_rent_3.rent_date = today - timedelta(days=6)
        movie_rent_3.updated_date = today - timedelta(days=2)
        movie_rent_3.cost = calculate_cost(movie_rent_3.rent_date, movie_rent_3.updated_date)
        movie_rent_3.save()

        response = client.get(reverse("profile"))
        self.assertEqual(response.data["#1"]["cost"], 3.5)
        self.assertEqual(response.data["#2"]["cost"], 5.0)
        self.assertEqual(response.data["#3"]["cost"], 4.0)
