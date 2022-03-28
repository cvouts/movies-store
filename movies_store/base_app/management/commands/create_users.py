from django.core.management.base import BaseCommand
from base_app.models import User

class Command(BaseCommand):
    def handle(self, *args, **options):
        if len(User.objects.filter(username="superuser")) > 0:
            self.stdout.write(self.style.ERROR("Users already exist"))
            return
        User.objects.create_superuser(username="superuser", password="password")
        User.objects.create_user(username="user", password="password")
        self.stdout.write(self.style.SUCCESS("Superuser \"superuser\" and user \"user\" have been created"))
