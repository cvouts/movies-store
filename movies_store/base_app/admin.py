from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Movie, User, RentMovie

class RentMovieAdmin(admin.ModelAdmin):
    readonly_fields = ('rent_date',)

# Register your models here.
admin.site.register(Movie)
admin.site.register(User, UserAdmin)
admin.site.register(RentMovie, RentMovieAdmin)
