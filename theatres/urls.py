from django.urls import path, include
from .views import index, view_movies

urlpatterns = [
    path('', index, name='theatres-view'),
    path('<int:id>', view_movies, name='theatres-movies-view'),
]
