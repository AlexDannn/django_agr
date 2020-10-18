from django.urls import path
from . import views
from users import views as user_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.scrap_list_view, name='home'),
    path('movies/', views.movie_list_view, name='movies'),
    path('games/', views.games_list_view, name='games'),
    path('sports/', views.sports_list_view, name='sports'),
    path('hacks/', views.hacks_list_view, name='hacks'),
    path('about/', views.about, name='scrap-about'),
    ]