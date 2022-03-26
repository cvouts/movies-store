from django.test import TestCase
from django.urls import reverse
from base_app.models import Movie, RentMovie, User
from rest_framework.test import APIClient

class ProfileViewTest(TestCase):
    def setUp(self):
        movie_1 = Movie.objects.create(title="Lord of the Rings", category="Fantasy", rating=9)
        movie_2 = Movie.objects.create(title="Matrix", category="Sci-Fi", rating=7)
        movie_3 = Movie.objects.create(title="Narnia", category="Fantasy", rating=6)
        movie_4 = Movie.objects.create(title="Warcraft", category="Fantasy", rating=6)
        movie_1.save()
        movie_2.save()
        movie_3.save()
        movie_4.save()

        user = User.objects.create_user(username="user", password="password")
        user.save()

        movie_rent_1 = RentMovie.objects.create(user=user, movie=movie_1, status="rented_currently")
        movie_rent_2 = RentMovie.objects.create(user=user, movie=movie_2, status="rented_currently")
        movie_rent_3 = RentMovie.objects.create(user=user, movie=movie_4, status="rented_previously")
        movie_rent_1.save()
        movie_rent_2.save()
        movie_rent_3.save()

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

    def test_profile(self):
        client = APIClient()
        user = User.objects.get(username="user")
        client.force_authenticate(user=user)

        response = client.get(reverse("profile"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)

        response = client.get(reverse("profile"), {"category": "Fantasy"})
        self.assertEqual(len(response.data), 2)

        response = client.get(reverse("profile"), {"category": "not_a_category"})
        self.assertEqual(len(response.data), 0)

        response = client.get(reverse("profile"), {"status": "rented_currently"})
        self.assertEqual(len(response.data), 2)

        response = client.get(reverse("profile"), {"status": "rented_previously"})
        self.assertEqual(len(response.data), 1)

        response = client.get(reverse("profile"), {"status": "not_a_status"})
        self.assertEqual(len(response.data), 0)

        response = client.get(reverse("profile"),
                               {"status": "rented_previously",
                                "category": "Fantasy"})
        self.assertEqual(len(response.data), 1)

        response = client.get(reverse("profile"), {"rating" : 9.0})
        self.assertEqual(len(response.data), 1)
