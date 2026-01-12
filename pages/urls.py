from django.urls import path, include
from .views import home, about, booking, contact, login, signup, movies, movie_detail, logout, movies_by_genre

urlpatterns = [
    path('', home, name='home'),
    path('about', about, name='about'),
    path('booking', booking, name='booking'),
    path('movies', movies, name='movies'),
    path('movie/<int:id>', movie_detail, name='movie_detail'),
    path('contact', contact, name='contact'),
    path('login', login, name='login'),
    path('signup', signup, name='signup'),
    path('logout', logout, name='logout'),
    path('category/<str:genre>', movies_by_genre, name='movies_by_genre'),
]
