import mock

from django.urls import reverse
from django.core.files import File
from rest_framework import status
from rest_framework.test import APITestCase

from datetime import date

from .models import Movie, Category, Actor, Genre, Rating, RatingStar, Review


class MoviesAPITestCase(APITestCase):
    def setUp(self) -> None:
        file_mock = mock.MagicMock(spec=File)
        file_mock.name = 'test_poster.jpg'

        self.genre = Genre.objects.create(
            title='test genre',
            description='Test test test',
            slug='test-genre'
        )

        self.director = Actor.objects.create(
            name='Test director',
            age=100,
            description='Testtest',
            image=file_mock.name
        )

        self.actor = Actor.objects.create(
            name='Test actor',
            age=100,
            description='Testtest',
            image=file_mock.name
        )

        self.category = Category.objects.create(
            title='TestCategory',
            description='test test',
            slug='test-category'
        )

        self.movie = Movie(
            id=1,
            title='TestTitle',
            tagline='TestTagLine',
            description='Test test test',
            poster=file_mock.name,
            year=2150,
            country='Babylon',
            world_premiere=date.today(),
            budget=100,
            fees_in_usa=150,
            fees_in_world=200,
            category=self.category,
            slug='test-movie',
            draft=False
        )
        self.movie.directors.add(self.director)
        self.movie.actors.add(self.actor)
        self.movie.genres.add(self.genre)
        self.movie.save()

        self.star = RatingStar.objects.create(value=5)

        self.rating = Rating.objects.create(
            ip='172.17.0.1',
            star=self.star,
            movie=self.movie
        )

        self.review = Review.objects.create(
            id=3,
            email='test@gmail.com',
            name='TestName',
            text='Test test test',
            movie=self.movie
        )

        self.review_data = {
            "email": "reviewdata@gmail.com",
            "name": "Name",
            "text": 'Test review',
            "movie": 1
        }

        self.children_review_data = {
            "email": "children@gmail.com",
            "name": "Children name",
            "text": 'Test review',
            "parent": 3,
            "movie": 1
        }

        self.rating_data = {
            "movie": 1
        }

    def test_movies_list(self):
        response = self.client.get(reverse('movies_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['count'], 1)
        self.assertEqual(response.json().get('results')[0].get('title'), 'TestTitle')

    def test_movie_detail(self):
        response = self.client.get(reverse('movie_detail', kwargs={'pk': self.movie.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('title'), 'TestTitle')
        self.assertEqual(response.json().get('reviews')[0].get('name'), self.review.name)

    def test_fail_movie_detail(self):
        response = self.client.get(reverse('movie_detail', kwargs={'pk': 20}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_actors_list(self):
        response = self.client.get(reverse('actors_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['count'], 2)
        self.assertEqual(response.json().get('results')[0].get('name'), 'Test director')

    def test_actor_detail(self):
        response = self.client.get(reverse('actor_detail', kwargs={'pk': self.actor.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('name'), 'Test actor')

    def test_fail_actor_detail(self):
        response = self.client.get(reverse('actor_detail', kwargs={'pk': 20}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_review_create(self):
        response = self.client.post(reverse('review_create'), self.review_data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(len(Review.objects.all()) == 2)

    def test_children_review_create(self):
        response = self.client.post(reverse('review_create'), self.children_review_data, format='multipart')
        parent = Review.objects.get(pk=3)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(len(Review.objects.all()) == 2)
        self.assertEqual(parent.children.first().name, self.children_review_data['name'])

    def test_get_middle_rating(self):
        response = self.client.get(reverse('movies_list'))
        self.assertEqual(response.json().get('results')[0].get('middle_star'), 5)

    def test_rating_add(self):
        RatingStar.objects.create(value=3)

        self.rating_data["star"] = 3
        response = self.client.post(reverse('rating_add'), self.rating_data, format='multipart')
        movies_list = self.client.get(reverse('movies_list'))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(len(Rating.objects.all()) == 2)
        self.assertEqual(movies_list.json().get('results')[0].get('middle_star'), 4)
