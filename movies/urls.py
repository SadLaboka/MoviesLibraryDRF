from django.urls import path

from . import views


urlpatterns = [
    path("movie/", views.MovieListView.as_view()),
    path("movie/<str:slug>/", views.MovieDetailView.as_view()),
]
