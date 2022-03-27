from django.core.management.base import BaseCommand
from base_app.models import Movie

class Command(BaseCommand):
    def handle(self, *args, **options):
        Movie.objects.create(title="The Shawshank Redemption", category="Drama",
                             rating=9.3)
        Movie.objects.create(title="The Lord of the Rings: The Return of the King", category="Fantasy",
                             rating=9.0)
        Movie.objects.create(title="The Godfather", category="Crime",
                             rating=9.2)
        Movie.objects.create(title="The Dark Knight", category="Superhero",
                             rating=9.1)
        Movie.objects.create(title="Pulp Fiction", category="Crime",
                             rating=8.9)
        Movie.objects.create(title="Inception", category="Sci-Fi",
                             rating=8.8)


        self.stdout.write(self.style.SUCCESS("Successfully populated the database!"))
