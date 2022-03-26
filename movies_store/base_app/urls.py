from django.urls import path
from .views import MoviesView, RentMovieView, ReturnMovieView, ProfileView

urlpatterns = [
    path('movies', MoviesView.as_view(), name='movies'),
    path('movies/<int:id>', MoviesView.as_view(), name='movie_details'),
    path('rent', RentMovieView.as_view(), name='rent'),
    path('return', ReturnMovieView.as_view(), name='return'),
    path('profile', ProfileView.as_view(), name='profile')
]
