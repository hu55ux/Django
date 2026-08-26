# from django.contrib import admin
from django.urls import path, include

from notes import views as notes_views

urlpatterns = [
    #    path('admin/', admin.site.urls),
    # / -> home
    path("", notes_views.home, name="home"),
# / /notes/ -> routes from notes/urls.py
    path("notes/", include("notes.urls")),
]
