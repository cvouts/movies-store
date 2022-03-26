from django.test import TestCase
from django.urls import reverse
from base_app.models import Movie, User
from rest_framework.test import APIClient

class MoviesViewTest(TestCase):
    def setUp(self):
        movie_1 = Movie.objects.create(title="Lord of the Rings", category="Fantasy")
        movie_2 = Movie.objects.create(title="Matrix", category="Sci-Fi")
        movie_3 = Movie.objects.create(title="Narnia", category="Fantasy")
        movie_1.save()
        movie_2.save()
        movie_3.save()

        user_1 = User.objects.create_superuser(username="user_1", password="password")
        user_2 = User.objects.create_user(username="user_2", password="password")

        user_1.save()
        user_2.save()

    def test_simple_get(self):
        response = self.client.get(reverse("movies"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)

    def test_category_parameter(self):
        response = self.client.get(reverse("movies"), {"category": "Fantasy"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_get_movie_details(self):
        response = self.client.get(reverse("movie_details", kwargs={"id" : "1"}))
        self.assertEqual(response.data["title"], "Lord of the Rings")

    def test_post(self):
        response = self.client.post(reverse("movies"), {"title" : "Star Wars"})
        self.assertEqual(response.status_code, 401)

        client = APIClient()

        user = User.objects.get(username="user_2")
        client.force_authenticate(user=user)
        response = client.post(reverse("movies"), {"title" : "Star Wars", "category" : "Fantasy"})
        self.assertEqual(response.status_code, 403)

        user = User.objects.get(username="user_1")
        client.force_authenticate(user=user)
        response = client.post(reverse("movies"), {"title" : "Star Wars", "category" : "Fantasy"})
        self.assertEqual(response.status_code, 201)

    def test_patch(self):

        response = self.client.patch(reverse("movie_details", kwargs={"id" : "1"}), {"details" : "best movie ever!"})
        self.assertEqual(response.status_code, 401)
        movie = Movie.objects.get(id=1)
        self.assertEqual(movie.details, None)

        client = APIClient()

        user = User.objects.get(username="user_2")
        client.force_authenticate(user=user)
        response = client.patch(reverse("movie_details", kwargs={"id" : "1"}), {"details" : "best movie ever!"})
        self.assertEqual(response.status_code, 403)
        movie = Movie.objects.get(id=1)
        self.assertEqual(movie.details, None)

        user = User.objects.get(username="user_1")
        client.force_authenticate(user=user)
        response = client.patch(reverse("movie_details", kwargs={"id" : "1"}), {"details" : "best movie ever!"})
        self.assertEqual(response.status_code, 202)
        movie = Movie.objects.get(id=1)
        self.assertEqual(movie.details, "best movie ever!")

    def test_delete(self):
        response = self.client.delete(reverse("movie_details", kwargs={"id" : "2"}))
        self.assertEqual(response.status_code, 401)
        movies = Movie.objects.all()
        self.assertEqual(len(movies), 3)

        client = APIClient()

        user = User.objects.get(username="user_2")
        client.force_authenticate(user=user)
        response = client.delete(reverse("movie_details", kwargs={"id" : "2"}))
        self.assertEqual(response.status_code, 403)
        movies = Movie.objects.all()
        self.assertEqual(len(movies), 3)

        user = User.objects.get(username="user_1")
        client.force_authenticate(user=user)
        response = client.delete(reverse("movie_details", kwargs={"id" : "2"}))
        self.assertEqual(response.status_code, 202)
        movies = Movie.objects.all()
        self.assertEqual(len(movies), 2)

        response = client.delete(reverse("movie_details", kwargs={"id" : "4"}))
        self.assertEqual(response.status_code, 404)
