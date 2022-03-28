from django.test import TestCase
from django.urls import reverse
from base_app.models import Movie, RentMovie, User
from rest_framework.test import APIClient

class RentViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username="user", password="password")
        Movie.objects.create(title="Lord of the Rings", category="Fantasy",
                             rating=8.0)
        Movie.objects.create(title="Matrix", category="Sci-Fi", rating=8.0)
        Movie.objects.create(title="Narnia", category="Fantasy", rating=6.0)

    def test_other_methods(self):
        response = self.client.get(reverse("rent"), {"movie" : "1"})
        self.assertEqual(response.status_code, 405)
        response = self.client.patch(reverse("rent"), {"movie" : "1"})
        self.assertEqual(response.status_code, 405)
        response = self.client.delete(reverse("rent"), {"movie" : "1"})
        self.assertEqual(response.status_code, 405)

    def test_not_logged_in(self):
        response = self.client.post(reverse("rent"), {"movie" : "1"})
        self.assertEqual(response.status_code, 401)

    def login(self):
        client = APIClient()
        user = User.objects.get(username="user")
        client.force_authenticate(user=user)
        return client

    def test_rent_404(self):
        client = self.login()
        response = client.post(reverse("rent"), {"movie" : "1221"})
        self.assertEqual(response.status_code, 404)

    def test_rent_202_then_400(self):
        client = self.login()
        user = User.objects.get(username="user")
        movies = RentMovie.objects.filter(user=user,
                                          movie=Movie.objects.get(id=1),
                                          status="rented_currently")
        self.assertEqual(len(movies), 0)
        response = client.post(reverse("rent"), {"movie" : "1"})
        self.assertEqual(response.status_code, 202)
        movies = RentMovie.objects.filter(user=user,
                                          movie=Movie.objects.get(id=1),
                                          status="rented_currently")
        self.assertEqual(len(movies), 1)

        response = client.post(reverse("rent"), {"movie" : "1"})
        self.assertEqual(response.status_code, 400)
