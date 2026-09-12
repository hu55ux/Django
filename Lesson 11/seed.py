import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from movies.models import Movie

def seed_data():
    print("Seeding database...")

    # 1. Create Superuser
    admin_user, created = User.objects.get_or_create(username='admin', defaults={
        'email': 'admin@example.com',
        'is_staff': True,
        'is_superuser': True,
        'first_name': 'Admin',
        'last_name': 'User'
    })
    if created:
        admin_user.set_password('adminpassword123')
        admin_user.save()
        print(" -> Created Superuser 'admin' (password: adminpassword123)")
    else:
        print(" -> Superuser 'admin' already exists.")

    # 2. Create Demo User 1
    u1, created = User.objects.get_or_create(username='user1', defaults={
        'first_name': 'Əli',
        'last_name': 'Məmmədov',
        'email': 'user1@example.com'
    })
    if created:
        u1.set_password('user1password123')
        u1.save()
        print(" -> Created User 'user1' (password: user1password123)")

    # 3. Create Demo User 2
    u2, created = User.objects.get_or_create(username='user2', defaults={
        'first_name': 'Leyla',
        'last_name': 'Hüseynova',
        'email': 'user2@example.com'
    })
    if created:
        u2.set_password('user2password123')
        u2.save()
        print(" -> Created User 'user2' (password: user2password123)")

    # 4. Add Movies for User 1
    movies_u1 = [
        {
            'title': 'Inception',
            'genre': 'Sci-Fi',
            'release_year': 2010,
            'status': Movie.STATUS_WATCHED,
            'rating': 10,
        },
        {
            'title': 'The Dark Knight',
            'genre': 'Action',
            'release_year': 2008,
            'status': Movie.STATUS_WATCHED,
            'rating': 9,
        },
        {
            'title': 'Dune: Part Two',
            'genre': 'Sci-Fi',
            'release_year': 2024,
            'status': Movie.STATUS_WATCHING,
            'rating': 9,
        },
        {
            'title': 'Oppenheimer',
            'genre': 'Drama',
            'release_year': 2023,
            'status': Movie.STATUS_WANT_TO_WATCH,
            'rating': 8,
        },
    ]

    for data in movies_u1:
        movie, created = Movie.objects.get_or_create(
            title=data['title'],
            owner=u1,
            defaults=data
        )
        if created:
            print(f"   + Added movie for {u1.username}: {movie.title}")

    # 5. Add Movies for User 2
    movies_u2 = [
        {
            'title': 'Interstellar',
            'genre': 'Sci-Fi',
            'release_year': 2014,
            'status': Movie.STATUS_WATCHED,
            'rating': 10,
        },
        {
            'title': 'Parasite',
            'genre': 'Thriller',
            'release_year': 2019,
            'status': Movie.STATUS_WATCHED,
            'rating': 9,
        },
        {
            'title': 'Spirited Away',
            'genre': 'Animation',
            'release_year': 2001,
            'status': Movie.STATUS_WANT_TO_WATCH,
            'rating': 10,
        },
    ]

    for data in movies_u2:
        movie, created = Movie.objects.get_or_create(
            title=data['title'],
            owner=u2,
            defaults=data
        )
        if created:
            print(f"   + Added movie for {u2.username}: {movie.title}")

    print("Database seeding completed successfully!")

if __name__ == '__main__':
    seed_data()
