from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('movies/', views.movies_list, name='movies_list'),
    path('movies/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('movies/<int:movie_id>/book/', views.book_ticket, name='book_ticket'),
    path('bookings/', views.bookings_list, name='bookings_list'),
]
