from django.test import TestCase
from django.urls import reverse
from . import data


class CinemaViewsTestCase(TestCase):
    def test_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "CineMagic Kinoteatrı")
        self.assertContains(response, "Home")
        self.assertContains(response, "Movies")
        self.assertContains(response, "Bookings")

    def test_movies_list_page(self):
        response = self.client.get(reverse('movies_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Inception")
        self.assertContains(response, "SOLD OUT")

    def test_movies_list_filtering(self):
        response = self.client.get(reverse('movies_list') + '?genre=Action')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "The Dark Knight")
        self.assertNotContains(response, "Inception")

    def test_movies_list_available_only_filter(self):
        response = self.client.get(reverse('movies_list') + '?available_only=on')
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Interstellar")  # Interstellar has 0 seats

    def test_movie_detail_page_existing(self):
        response = self.client.get(reverse('movie_detail', kwargs={'movie_id': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Inception")
        self.assertContains(response, "Book ticket")

    def test_movie_detail_page_not_found(self):
        response = self.client.get(reverse('movie_detail', kwargs={'movie_id': 999}))
        self.assertEqual(response.status_code, 404)
        self.assertContains(response, "Movie not found", status_code=404)

    def test_book_ticket_validation_empty_name(self):
        response = self.client.post(
            reverse('book_ticket', kwargs={'movie_id': 1}),
            {'customer_name': '', 'ticket_count': '2'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Müştərinin adı boş ola bilməz.")

    def test_book_ticket_validation_sold_out(self):
        # Movie 3 is Interstellar with 0 seats
        response = self.client.post(
            reverse('book_ticket', kwargs={'movie_id': 3}),
            {'customer_name': 'Leyla', 'ticket_count': '1'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "SOLD OUT")

    def test_book_ticket_success(self):
        movie_before = data.get_movie_by_id(1)
        seats_before = movie_before["available_seats"]

        response = self.client.post(
            reverse('book_ticket', kwargs={'movie_id': 1}),
            {'customer_name': 'Məmməd Məmmədov', 'ticket_count': '3'}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Biletiniz Uğurla Bron Olundu!")
        self.assertContains(response, "Məmməd Məmmədov")
        self.assertContains(response, "Inception")

        movie_after = data.get_movie_by_id(1)
        self.assertEqual(movie_after["available_seats"], seats_before - 3)
