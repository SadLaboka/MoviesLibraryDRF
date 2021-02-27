from django.urls import path

from . import views


urlpatterns = [
    path("movie/", views.MovieListView.as_view()),
    path("movie/<str:slug>/", views.MovieDetailView.as_view()),
    path("review/", views.ReviewCreateView.as_view()),
    path("rating/", views.AddStarRatingView.as_view()),
]
