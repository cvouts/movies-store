from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Movie, User

# Register your models here.
admin.site.register(Movie)
admin.site.register(User, UserAdmin)
