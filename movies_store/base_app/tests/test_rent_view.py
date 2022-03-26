from django.test import TestCase
from django.urls import reverse
from base_app.models import Movie, RentMovie, User
from rest_framework.test import APIClient

class RentViewTest(TestCase):
    def setUp(self):
        movie_1 = Movie.objects.create(title="Lord of the Rings", category="Fantasy", rating=9)
        movie_2 = Movie.objects.create(title="Matrix", category="Sci-Fi", rating=8)
        movie_3 = Movie.objects.create(title="Narnia", category="Fantasy", rating=7)
        movie_1.save()
        movie_2.save()
        movie_3.save()

        user = User.objects.create_user(username="user", password="password")
        user.save()

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

    def test_rent(self):
        client = APIClient()
        user = User.objects.get(username="user")
        client.force_authenticate(user=user)

        response = client.post(reverse("rent"), {"movie" : "1221"})
        self.assertEqual(response.status_code, 404)

        movies = RentMovie.objects.filter(user=user, movie=Movie.objects.get(id=1), status="rented_currently")
        self.assertEqual(len(movies), 0)
        response = client.post(reverse("rent"), {"movie" : "1"})
        self.assertEqual(response.status_code, 202)
        movies = RentMovie.objects.filter(user=user, movie=Movie.objects.get(id=1), status="rented_currently")
        self.assertEqual(len(movies), 1)

        response = client.post(reverse("rent"), {"movie" : "1"})
        self.assertEqual(response.status_code, 400)
