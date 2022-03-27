from django.core.management.base import BaseCommand
from base_app.models import Movie

class Command(BaseCommand):
    def handle(self, *args, **options):
        for movie in Movie.objects.all():
            movie.delete()


        self.stdout.write(self.style.ERROR("Successfully depopulated the database!"))
