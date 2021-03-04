from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

from . import views


urlpatterns = format_suffix_patterns([
    path("movie/", views.MovieViewSet.as_view({'get': 'list'}), name='movies_list'),
    path("movie/<int:pk>/", views.MovieViewSet.as_view({'get': 'retrieve'}), name='movie_detail'),
    path("review/", views.ReviewCreateViewSet.as_view({'post': 'create'}), name='review_create'),
    path("rating/", views.AddStarRatingViewSet.as_view({'post': 'create'}), name='rating_add'),
    path('actor/', views.ActorViewSet.as_view({'get': 'list'}), name='actors_list'),
    path('actor/<int:pk>/', views.ActorViewSet.as_view({'get': 'retrieve'}), name='actor_detail'),
])


# urlpatterns = [
#     path("movie/", views.MovieListView.as_view()),
#     path("movie/<int:pk>/", views.MovieDetailView.as_view()),
#     path("review/", views.ReviewCreateView.as_view()),
#     path("rating/", views.AddStarRatingView.as_view()),
#     path("actors/", views.ActorsListView.as_view()),
#     path("actors/<int:pk>/", views.ActorsDetailView.as_view()),
# ]
