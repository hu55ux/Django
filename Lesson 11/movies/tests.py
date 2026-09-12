from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Movie
from .forms import MovieForm

class MovieModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.movie = Movie.objects.create(
            title='Inception',
            genre='Sci-Fi',
            release_year=2010,
            status=Movie.STATUS_WATCHED,
            rating=10,
            owner=self.user
        )

    def test_movie_str(self):
        self.assertEqual(str(self.movie), 'Inception (2010)')

    def test_movie_fields(self):
        self.assertEqual(self.movie.owner, self.user)
        self.assertEqual(self.movie.rating, 10)
        self.assertEqual(self.movie.status, 'watched')


class MovieFormTest(TestCase):
    def test_valid_form(self):
        form_data = {
            'title': 'The Matrix',
            'genre': 'Sci-Fi',
            'release_year': 1999,
            'status': 'watched',
            'rating': 9,
        }
        form = MovieForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_release_year(self):
        form_data = {
            'title': 'Ancient Film',
            'genre': 'Drama',
            'release_year': 1800, # before 1888
            'status': 'want_to_watch',
            'rating': 5,
        }
        form = MovieForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('release_year', form.errors)

    def test_invalid_rating(self):
        form_data = {
            'title': 'Super Movie',
            'genre': 'Action',
            'release_year': 2020,
            'status': 'watching',
            'rating': 15, # > 10
        }
        form = MovieForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('rating', form.errors)


class MovieAuthorizationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='user1', password='passuser1')
        self.user2 = User.objects.create_user(username='user2', password='passuser2')

        self.movie1 = Movie.objects.create(
            title='User1 Movie',
            genre='Action',
            release_year=2021,
            status='watching',
            rating=8,
            owner=self.user1
        )
        self.movie2 = Movie.objects.create(
            title='User2 Movie',
            genre='Drama',
            release_year=2022,
            status='watched',
            rating=9,
            owner=self.user2
        )

    def test_unauthenticated_access_redirects(self):
        response = self.client.get(reverse('movie_list'))
        self.assertRedirects(response, f"/login/?next={reverse('movie_list')}")

    def test_user_only_sees_own_movies(self):
        self.client.login(username='user1', password='passuser1')
        response = self.client.get(reverse('movie_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'User1 Movie')
        self.assertNotContains(response, 'User2 Movie')

    def test_user_cannot_edit_other_user_movie(self):
        self.client.login(username='user1', password='passuser1')
        # user1 trying to edit user2's movie
        response = self.client.get(reverse('movie_update', kwargs={'pk': self.movie2.pk}))
        self.assertEqual(response.status_code, 404)

    def test_user_cannot_delete_other_user_movie(self):
        self.client.login(username='user1', password='passuser1')
        # user1 trying to delete user2's movie
        response = self.client.get(reverse('movie_delete', kwargs={'pk': self.movie2.pk}))
        self.assertEqual(response.status_code, 404)

    def test_status_filter(self):
        self.client.login(username='user1', password='passuser1')
        response = self.client.get(reverse('movie_list') + '?status=watching')
        self.assertContains(response, 'User1 Movie')

        response_empty = self.client.get(reverse('movie_list') + '?status=watched')
        self.assertNotContains(response_empty, 'User1 Movie')
