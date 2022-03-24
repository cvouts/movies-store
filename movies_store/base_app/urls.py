from django.urls import path
from .views import MoviesView, RentView

urlpatterns = [
    path('movies/', MoviesView.as_view()),
    path('movies/<int:id>', MoviesView.as_view()),
    path('movies/<str:category>', MoviesView.as_view()),
    path('rent/<int:id>', RentView.as_view())
]
