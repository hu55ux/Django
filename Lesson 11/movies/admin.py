from django.contrib import admin
from .models import Movie

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'genre', 'release_year', 'status', 'rating', 'owner', 'created_at')
    list_filter = ('status', 'genre', 'created_at')
    search_fields = ('title', 'genre', 'owner__username', 'owner__email')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

    fieldsets = (
        ('Film Məlumatları', {
            'fields': ('title', 'genre', 'release_year', 'owner')
        }),
        ('Status və Qiymət', {
            'fields': ('status', 'rating')
        }),
        ('Tarix Məlumatları', {
            'fields': ('created_at',)
        }),
    )
