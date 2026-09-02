from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from . import data
from .forms import TicketBookingForm, MovieFilterForm


def home(request: HttpRequest) -> HttpResponse:
    context = {
        "cinema_name": "CineMagic Kinoteatrı",
        "welcome_text": "Xoş gəlmisiniz! Qabaqcıl kinoteatrımızda ən son filmlərə baxın və biletlərinizi asanlıqla bron edin.",
        "featured_movies": data.get_movies()[:3],
    }
    return render(request, "cinema/home.html", context)


def movies_list(request: HttpRequest) -> HttpResponse:
    filter_form = MovieFilterForm(request.GET or None)
    selected_genre = ""
    available_only = False

    if filter_form.is_valid():
        selected_genre = filter_form.cleaned_data.get("genre", "") or ""
        selected_genre = selected_genre.strip()
        available_only = bool(filter_form.cleaned_data.get("available_only"))

    movies = data.get_movies(genre=selected_genre, available_only=available_only)
    genres = data.get_all_genres()

    context = {
        "movies": movies,
        "genres": genres,
        "selected_genre": selected_genre,
        "available_only": available_only,
        "filter_form": filter_form,
    }
    return render(request, "cinema/movies_list.html", context)


def movie_detail(request: HttpRequest, movie_id: int) -> HttpResponse:
    movie = data.get_movie_by_id(movie_id)
    if movie is None:
        return render(request, "cinema/movie_not_found.html", {"movie_id": movie_id}, status=404)

    context = {
        "movie": movie,
    }
    return render(request, "cinema/movie_detail.html", context)


def book_ticket(request: HttpRequest, movie_id: int) -> HttpResponse:
    movie = data.get_movie_by_id(movie_id)
    if movie is None:
        return render(request, "cinema/movie_not_found.html", {"movie_id": movie_id}, status=404)

    if request.method == "POST":
        form = TicketBookingForm(request.POST, movie=movie)
        if form.is_valid():
            customer_name = form.cleaned_data["customer_name"]
            ticket_count = form.cleaned_data["ticket_count"]

            success, message, booking = data.book_ticket(movie_id, customer_name, ticket_count)
            if not success:
                form.add_error(None, message)
                return render(request, "cinema/book_ticket.html", {"movie": movie, "form": form})

            updated_movie = data.get_movie_by_id(movie_id)
            context = {
                "booking": booking,
                "movie": updated_movie,
            }
            return render(request, "cinema/booking_success.html", context)
    else:
        form = TicketBookingForm(movie=movie)

    context = {
        "movie": movie,
        "form": form,
    }
    return render(request, "cinema/book_ticket.html", context)


def bookings_list(request: HttpRequest) -> HttpResponse:
    bookings = data.get_all_bookings()
    context = {
        "bookings": bookings,
    }
    return render(request, "cinema/bookings_list.html", context)
