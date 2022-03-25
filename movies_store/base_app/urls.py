from django.urls import path
from .views import MoviesView, RentMovieView, ReturnMovieView, UserProfileView

urlpatterns = [
    path('movies', MoviesView.as_view()),
    path('movies/<int:id>', MoviesView.as_view()),
    path('rent', RentMovieView.as_view()),
    path('return', ReturnMovieView.as_view()),
    path('profile', UserProfileView.as_view())
]
