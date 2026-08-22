from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('day/', include('day.urls')),
    path('quote/', include('quotes.urls')),
]
