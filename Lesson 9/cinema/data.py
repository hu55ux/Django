from copy import deepcopy
from datetime import datetime
from typing import Any, Optional

MOVIES: list[dict[str, Any]] = [
    {
        "id": 1,
        "title": "Inception",
        "genre": "Sci-Fi",
        "duration": "148 dəq",
        "age_limit": "12+",
        "available_seats": 15,
        "description": "A thief who steals corporate secrets through dream-sharing technology is given the inverse task of planting an idea into the mind of a C.E.O."
    },
    {
        "id": 2,
        "title": "The Dark Knight",
        "genre": "Action",
        "duration": "152 dəq",
        "age_limit": "16+",
        "available_seats": 8,
        "description": "When the menace known as the Joker wreaks havoc and chaos on Gotham, Batman must accept one of the greatest psychological and physical tests of his ability."
    },
    {
        "id": 3,
        "title": "Interstellar",
        "genre": "Sci-Fi",
        "duration": "169 dəq",
        "age_limit": "12+",
        "available_seats": 0,
        "description": "A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival as Earth faces extinction."
    },
    {
        "id": 4,
        "title": "Dune: Part Two",
        "genre": "Adventure",
        "duration": "166 dəq",
        "age_limit": "16+",
        "available_seats": 20,
        "description": "Paul Atreides unites with Chani and the Fremen while seeking revenge against the conspirators who destroyed his family."
    },
    {
        "id": 5,
        "title": "Oppenheimer",
        "genre": "Drama",
        "duration": "180 dəq",
        "age_limit": "18+",
        "available_seats": 5,
        "description": "The story of American scientist J. Robert Oppenheimer and his role in the development of the atomic bomb."
    },
    {
        "id": 6,
        "title": "Avatar: The Way of Water",
        "genre": "Action",
        "duration": "192 dəq",
        "age_limit": "12+",
        "available_seats": 0,
        "description": "Jake Sully lives with his newfound family on Pandora. Once a familiar threat returns, Jake must work with Neytiri and the Na'vi race to protect their home."
    },
]

BOOKINGS: list[dict[str, Any]] = []
_booking_counter = 1


def get_movies(genre: Optional[str] = None, available_only: bool = False) -> list[dict[str, Any]]:
    result = deepcopy(MOVIES)

    if genre and genre.strip():
        result = [m for m in result if m["genre"].lower() == genre.strip().lower()]

    if available_only:
        result = [m for m in result if m["available_seats"] > 0]

    return result


def get_movie_by_id(movie_id: int) -> Optional[dict[str, Any]]:
    for movie in MOVIES:
        if movie["id"] == movie_id:
            return deepcopy(movie)
    return None


def get_all_genres() -> list[str]:
    genres = set(movie["genre"] for movie in MOVIES)
    return sorted(list(genres))


def get_all_bookings() -> list[dict[str, Any]]:
    return deepcopy(BOOKINGS)


def book_ticket(movie_id: int, customer_name: str, ticket_count: int) -> tuple[bool, str, Optional[dict[str, Any]]]:
    global _booking_counter
    
    clean_name = customer_name.strip()
    if not clean_name:
        return False, "Müştərinin adı boş ola bilməz.", None

    if ticket_count <= 0:
        return False, "Biletlərin sayı sıfırdan böyük olmalıdır.", None

    movie = None
    for m in MOVIES:
        if m["id"] == movie_id:
            movie = m
            break

    if not movie:
        return False, "Film tapılmadı.", None

    if movie["available_seats"] == 0:
        return False, "Bu film üçün biletlər bitmişdir (SOLD OUT).", None

    if ticket_count > movie["available_seats"]:
        return False, f"Kafi boş yer yoxdur! Mövcud yer sayı: {movie['available_seats']}", None

    movie["available_seats"] -= ticket_count

    booking = {
        "id": _booking_counter,
        "movie_id": movie["id"],
        "movie_title": movie["title"],
        "customer_name": clean_name,
        "ticket_count": ticket_count,
        "created_at": datetime.now()
    }
    _booking_counter += 1
    BOOKINGS.append(booking)

    return True, "Bilet uğurla bron olundu!", deepcopy(booking)
