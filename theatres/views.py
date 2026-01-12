from django.shortcuts import render, redirect
from django.http import HttpResponse

from theatres.models import Theatre


# Create your views here.
def index(request):
    return HttpResponse('Hello, world!')

def view_movies(request, id):
    theatre = (
        Theatre.objects.prefetch_related('movies')
        .get(id=id)
    )
    movies = theatre.movies.all()

    return render(request, 'theatres/movies.html', {'movies': movies, 'theatre': theatre})