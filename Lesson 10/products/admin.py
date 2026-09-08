from django.contrib import admin
from .models import Product, Review

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    readonly_fields = ('created_at',)
    fields = ('user', 'rating', 'text', 'created_at')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at', 'average_rating', 'review_count')
    search_fields = ('name', 'description')
    list_filter = ('created_at',)
    inlines = [ReviewInline]

    @admin.display(description="Rəy Sayı")
    def review_count(self, obj):
        return obj.reviews.count()


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('product__name', 'user__username', 'text')
    readonly_fields = ('created_at',)
