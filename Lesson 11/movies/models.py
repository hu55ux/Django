from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Movie(models.Model):
    STATUS_WANT_TO_WATCH = 'want_to_watch'
    STATUS_WATCHING = 'watching'
    STATUS_WATCHED = 'watched'

    STATUS_CHOICES = [
        (STATUS_WANT_TO_WATCH, 'Baxmaq istəyirəm'),
        (STATUS_WATCHING, 'Baxıram'),
        (STATUS_WATCHED, 'Baxmışam'),
    ]

    GENRE_CHOICES = [
        ('Action', 'Döyüş (Action)'),
        ('Comedy', 'Komediya (Comedy)'),
        ('Drama', 'Dram (Drama)'),
        ('Sci-Fi', 'Elmi fantastika (Sci-Fi)'),
        ('Horror', 'Dəhşət (Horror)'),
        ('Romance', 'Romantik (Romance)'),
        ('Thriller', 'Triller (Thriller)'),
        ('Animation', 'Animasiya (Animation)'),
        ('Documentary', 'Sənədli (Documentary)'),
        ('Adventure', 'Macəra (Adventure)'),
        ('Fantasy', 'Fantastika (Fantasy)'),
        ('Other', 'Digər'),
    ]

    title = models.CharField(max_length=200, verbose_name="Filmin adı")
    genre = models.CharField(max_length=50, choices=GENRE_CHOICES, verbose_name="Janr")
    release_year = models.PositiveIntegerField(verbose_name="Buraxılış ili")
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default=STATUS_WANT_TO_WATCH, 
        verbose_name="Status"
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name="Şəxsi qiymətləndirmə (1-10)",
        help_text="1 ilə 10 arasında bir qiymət daxil edin"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Əlavə olunma tarixi")
    owner = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='movies', 
        verbose_name="Filmin sahibi"
    )

    class Meta:
        verbose_name = "Film"
        verbose_name_plural = "Filmlər"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.release_year})"
