from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.db.models import Avg, Count
from .models import Movie
from .forms import MovieForm, RegisterForm

@login_required
def movie_list(request):
    """
    Səhifə 1: Mənim filmlərimin siyahısı
    Yalnız cari avtorizasiya olunmuş istifadəçinin filmlərini göstərir.
    Status və Janr üzrə filtrləmə imkanı var.
    """
    # Avtorizasiya: İstifadəçi yalnız öz filmlərini görməlidir
    movies = Movie.objects.filter(owner=request.user)

    selected_status = request.GET.get('status', '').strip()
    selected_genre = request.GET.get('genre', '').strip()
    search_query = request.GET.get('q', '').strip()

    # Statusa görə filtr
    if selected_status:
        movies = movies.filter(status=selected_status)

    # Janra görə filtr
    if selected_genre:
        movies = movies.filter(genre=selected_genre)

    # Axtarış
    if search_query:
        movies = movies.filter(title__icontains=search_query)

    # Statistika (İstifadəçinin bütün filmləri üzrə)
    all_user_movies = Movie.objects.filter(owner=request.user)
    stats = {
        'total': all_user_movies.count(),
        'want_to_watch': all_user_movies.filter(status=Movie.STATUS_WANT_TO_WATCH).count(),
        'watching': all_user_movies.filter(status=Movie.STATUS_WATCHING).count(),
        'watched': all_user_movies.filter(status=Movie.STATUS_WATCHED).count(),
        'avg_rating': all_user_movies.aggregate(Avg('rating'))['rating__avg'] or 0.0,
    }

    context = {
        'movies': movies,
        'selected_status': selected_status,
        'selected_genre': selected_genre,
        'search_query': search_query,
        'status_choices': Movie.STATUS_CHOICES,
        'genre_choices': Movie.GENRE_CHOICES,
        'stats': stats,
    }
    return render(request, 'movies/movie_list.html', context)


@login_required
def movie_create(request):
    """
    Səhifə 2: Film əlavə etmək
    ModelForm istifadə edir və sahibi avtomatik olaraq request.user edir.
    """
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            movie = form.save(commit=False)
            movie.owner = request.user # Filmin sahibi istifadəçi olmalıdır
            movie.save()
            messages.success(request, f'"{movie.title}" uğurla siyahınıza əlavə edildi!')
            return redirect('movie_list')
        else:
            messages.error(request, 'Formda xətalar var. Zəhmət olmasa təshih edin.')
    else:
        form = MovieForm()

    return render(request, 'movies/movie_form.html', {
        'form': form,
        'title': 'Yeni Film Əlavə Et',
        'btn_text': 'Əlavə et'
    })


@login_required
def movie_update(request, pk):
    """
    Səhifə 3: Filmi redaktə etmək
    Avtorizasiya: İstifadəçi yalnız öz filmlərini redaktə edə bilər (get_object_or_404 owner=request.user).
    """
    movie = get_object_or_404(Movie, pk=pk, owner=request.user)

    if request.method == 'POST':
        form = MovieForm(request.POST, instance=movie)
        if form.is_valid():
            form.save()
            messages.success(request, f'"{movie.title}" uğurla yeniləndi!')
            return redirect('movie_list')
        else:
            messages.error(request, 'Formda xətalar var. Zəhmət olmasa təshih edin.')
    else:
        form = MovieForm(instance=movie)

    return render(request, 'movies/movie_form.html', {
        'form': form,
        'movie': movie,
        'title': f'"{movie.title}" Redaktə Et',
        'btn_text': 'Yadda saxla'
    })


@login_required
def movie_delete(request, pk):
    """
    Səhifə 4: Filmi silmək
    Avtorizasiya: İstifadəçi yalnız öz filmlərini silə bilər.
    """
    movie = get_object_or_404(Movie, pk=pk, owner=request.user)

    if request.method == 'POST':
        title = movie.title
        movie.delete()
        messages.success(request, f'"{title}" siyahıdan silindi.')
        return redirect('movie_list')

    return render(request, 'movies/movie_confirm_delete.html', {'movie': movie})


def register_view(request):
    """
    İstifadəçi qeydiyyatı
    """
    if request.user.is_authenticated:
        return redirect('movie_list')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Xoş gəldiniz, {user.username}! Hesabınız uğurla yaradıldı.')
            return redirect('movie_list')
        else:
            messages.error(request, 'Qeydiyyat zamanı xəta baş verdi. Məlumatları yoxlayın.')
    else:
        form = RegisterForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    """
    İstifadəçi girişi
    """
    if request.user.is_authenticated:
        return redirect('movie_list')

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Xoş gəldiniz, {user.username}!')
            next_url = request.GET.get('next') or 'movie_list'
            return redirect(next_url)
        else:
            messages.error(request, 'İstifadəçi adı və ya şifrə yanlışdır.')
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    """
    İstifadəçi çıxışı
    """
    logout(request)
    messages.info(request, 'Sistemdən uğurla çıxdınız.')
    return redirect('login')
