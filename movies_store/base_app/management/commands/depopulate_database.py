from django.core.management.base import BaseCommand
from base_app.models import Movie

class Command(BaseCommand):
    def handle(self, *args, **options):

        if len(Movie.objects.all()) == 0:
            self.stdout.write(self.style.WARNING("Movie table already empty!"))
        else:
            for movie in Movie.objects.all():
                movie.delete()
            self.stdout.write(self.style.ERROR("Successfully depopulated the Movie table!"))
