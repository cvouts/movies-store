from django.test import TestCase
from django.urls import reverse
from base_app.models import Movie, User
from rest_framework.test import APIClient

class MoviesViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_superuser(username="superuser", password="password")
        User.objects.create_user(username="simple_user", password="password")

        Movie.objects.create(title="Lord of the Rings", category="Fantasy",
                             rating=8)
        Movie.objects.create(title="Matrix", category="Sci-Fi",
                             rating=8)
        Movie.objects.create(title="Narnia", category="Fantasy",
                             rating=6)

    def test_simple_get(self):
        response = self.client.get(reverse("movies"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)

    def test_detail_url(self):
        response = self.client.get(reverse("movies"))
        self.assertEqual(response.data[0]["details_url"], reverse("movie_details", kwargs={"id" : "1"}))

    def test_parameters_category(self):
        response = self.client.get(reverse("movies"), {"category": "Fantasy"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_parameters_rating(self):
        response = self.client.get(reverse("movies"), {"rating": 8.0})
        self.assertEqual(len(response.data), 2)

    def test_parameters_category_rating(self):
        response = self.client.get(reverse("movies"), {"category": "Fantasy", "rating": 8.0})
        self.assertEqual(len(response.data), 1)

    def test_get_movie_details_200(self):
        response = self.client.get(reverse("movie_details", kwargs={"id" : "1"}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["title"], "Lord of the Rings")

    def test_get_movie_details_404(self):
        response = self.client.get(reverse("movie_details", kwargs={"id" : "1211"}))
        self.assertEqual(response.status_code, 404)

    def test_post_not_logged_in(self):
        response = self.client.post(reverse("movies"), {"title" : "Star Wars", "rating" : "9"})
        self.assertEqual(response.status_code, 401)

    def test_post_not_superuser(self):
        client = APIClient()
        user = User.objects.get(username="simple_user")
        client.force_authenticate(user=user)
        response = client.post(reverse("movies"), {"title" : "Star Wars", "category" : "Fantasy", "rating" : "9"})
        self.assertEqual(response.status_code, 403)

    def test_post_superuser(self):
        client = APIClient()
        user = User.objects.get(username="superuser")
        client.force_authenticate(user=user)
        response = client.post(reverse("movies"), {"title" : "Star Wars", "category" : "Fantasy", "rating" : "9"})
        self.assertEqual(response.status_code, 201)

    def test_patch_not_logged_in(self):
        response = self.client.patch(reverse("movie_details", kwargs={"id" : "1"}), {"details" : "best movie ever!"})
        self.assertEqual(response.status_code, 401)
        movie = Movie.objects.get(id=1)
        self.assertEqual(movie.details, None)

    def test_patch_not_superuser(self):
        client = APIClient()
        user = User.objects.get(username="simple_user")
        client.force_authenticate(user=user)
        response = client.patch(reverse("movie_details", kwargs={"id" : "1"}), {"details" : "best movie ever!"})
        self.assertEqual(response.status_code, 403)
        movie = Movie.objects.get(id=1)
        self.assertEqual(movie.details, None)

    def test_patch_superuser_202(self):
        client = APIClient()
        user = User.objects.get(username="superuser")
        client.force_authenticate(user=user)
        response = client.patch(reverse("movie_details", kwargs={"id" : "1"}),
                                {"details" : "best movie ever!"})
        self.assertEqual(response.status_code, 202)
        movie = Movie.objects.get(id=1)
        self.assertEqual(movie.details, "best movie ever!")

    def test_patch_superuser_404(self):
        client = APIClient()
        user = User.objects.get(username="superuser")
        client.force_authenticate(user=user)
        response = client.patch(reverse("movie_details", kwargs={"id" : "99"}),
                                {"details" : "best movie ever!"})
        self.assertEqual(response.status_code, 404)

    def test_delete_not_logged_in(self):
        response = self.client.delete(reverse("movie_details", kwargs={"id" : "2"}))
        self.assertEqual(response.status_code, 401)
        movies = Movie.objects.all()
        self.assertEqual(len(movies), 3)

    def test_delete_not_superuser(self):
        client = APIClient()
        user = User.objects.get(username="simple_user")
        client.force_authenticate(user=user)
        response = client.delete(reverse("movie_details", kwargs={"id" : "2"}))
        self.assertEqual(response.status_code, 403)
        movies = Movie.objects.all()
        self.assertEqual(len(movies), 3)

    def test_delete_superuser_202(self):
        client = APIClient()
        user = User.objects.get(username="superuser")
        client.force_authenticate(user=user)
        response = client.delete(reverse("movie_details", kwargs={"id" : "2"}))
        self.assertEqual(response.status_code, 202)
        movies = Movie.objects.all()
        self.assertEqual(len(movies), 2)

    def test_delete_superuser_202(self):
        client = APIClient()
        user = User.objects.get(username="superuser")
        client.force_authenticate(user=user)
        response = client.delete(reverse("movie_details", kwargs={"id" : "99"}))
        self.assertEqual(response.status_code, 404)
