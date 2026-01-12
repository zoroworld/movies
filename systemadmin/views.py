from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import NewUser
from movies.models import Movie
from bookings.models import Booking
from theatres.models import Theatre, Seat, Location, Show, TimeSlot
from cities_light.models import Country, Region, City


# Create your views here.
def admin(request):
    return render(request, 'systemadmin/dashboard.html')


def movies(request):
    movies = Movie.objects.all()
    return render(request, 'systemadmin/movies.html', {'movies': movies})


def create_movies(request):
    if request.method == "POST":
        title = request.POST['title']
        description = request.POST['description']
        genre = request.POST['genre']
        release_date = request.POST['release_date']
        poster = request.FILES.get('poster')

        # First, create the movie
        movie = Movie.objects.create(
            title=title,
            description=description,
            genre=genre,
            release_date=release_date,
            poster=poster,
        )

        return redirect('dashboard-movies-view')

    genres = Movie.Genre.choices
    return render(request, 'systemadmin/create-movies.html', {'genres': genres})


def edit_movies(request, id):
    movie = Movie.objects.get(id=id)
    if request.method == "POST":
        title = request.POST['title']
        description = request.POST['description']
        genre = request.POST['genre']
        realease_date = request.POST['date']
        movie.title = title
        movie.description = description
        movie.genre = genre
        movie.save()
        return redirect('dashboard-movies-view')
    return render(request, 'systemadmin/edit-movies.html', {'movie': movie})


def theaters(request):
    theaters_all = Theatre.objects.prefetch_related('seats', 'shows__movie').all()
    return render(request, 'systemadmin/theaters.html', {'theaters': theaters_all})


def create_theaters(request):
    if request.method == "POST":
        name = request.POST['name']
        description = request.POST['description']

        movies_ids = request.POST.getlist('movie')  # list of movie IDs
        num_seats = int(request.POST.get('seats'))

        # location
        locations = Location.objects.create(
            country_id=request.POST.get('country'),
            state_id=request.POST.get('state'),
            city_id=request.POST.get('city')
        )

        theatre = Theatre.objects.create(
            name=name,
            description=description,
            location=locations
        )

        theatre.movies.set(movies_ids)

        seat_list = []
        for seat_num in range(1, num_seats + 1):
            list_data = Seat.objects.create(
                seat=seat_num
            )
            seat_list.append(list_data)
        theatre.movies.set(movies_ids)
        theatre.seats.set(seat_list)
        return redirect('dashboard-theaters-view')
    else:
        movies = Movie.objects.all()
        countries = Country.objects.all().order_by('name')
        return render(request, 'systemadmin/create-theaters.html', {'countries': countries, 'movies': movies})


def load_states(request):
    country_id = request.GET.get('country_id')
    states = Region.objects.filter(country_id=country_id).order_by('name')
    return JsonResponse(list(states.values('id', 'name')), safe=False)


def load_cities(request):
    state_id = int(request.GET.get('state_id'))
    cities = City.objects.filter(region_id=state_id)
    print(f"Number of cities in state {state_id}: {cities.count()}")
    return JsonResponse(list(cities.values('id', 'name')), safe=False)


def edit_theaters(request, id):
    return render(request, 'systemadmin/edit-theaters.html', {'id': id})


def delete_theaters(request, id):
    delete_theater = Theatre.objects.get(id=id)
    delete_theater.delete()
    return redirect('dashboard-theaters-view')


def delete_movies(request, id):
    movie = Movie.objects.get(id=id)
    movie.delete()
    return redirect('dashboard-movies-view')


def users(request):
    users = NewUser.objects.all()
    return render(request, 'systemadmin/users.html', {'users': users})


def edit_users(request, id):
    user = NewUser.objects.get(id=id)

    if request.method == "POST":
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.phone = request.POST.get('phone')

        # Handle profile picture only if uploaded
        if 'profile_pic' in request.FILES:
            user.profile_pic = request.FILES['profile_pic']

        user.save()

        return redirect('dashboard-users-view')

    return render(request, 'your_template.html', {'user': user})


def delete_users(request, id):
    try:
        user = NewUser.objects.get(id=id)
        user.delete()
    except NewUser.DoesNotExist:
        pass  # or show error message

    return redirect('dashboard-user-view')


def booking_history(request):
    bookings = Booking.objects.all()
    return render(request, 'systemadmin/booking-history.html', {'bookings': bookings})


# your Show model
def create_show(request):
    if request.method == "POST":
        theatre = get_object_or_404(Theatre, id=request.POST.get("theatre_id"))

        movie_ids = request.POST.getlist("movie_ids[]")
        dates = request.POST.getlist("dates[]")
        start_times = request.POST.getlist("start_times[]")
        end_times = request.POST.getlist("end_times[]")

        for movie_id, show_date, start, end in zip(
                movie_ids, dates, start_times, end_times
        ):
            movie = get_object_or_404(Movie, id=movie_id)

            # Create or reuse TimeSlot
            time_slot, _ = TimeSlot.objects.get_or_create(
                start_time=start,
                end_time=end
            )

            # Create or update Show
            Show.objects.update_or_create(
                theatre=theatre,
                movie=movie,
                date=show_date,
                time_slot=time_slot,
                defaults={
                    "is_available": True
                }
            )

        return redirect('dashboard-theaters-view')

    shows = Show.objects.all()
    return render(request, "systemadmin/theaters.html", {'shows': shows})


def get_profile(request, id):
    user = NewUser.objects.get(id=id)
    if not user:
        return redirect('dashboard-user-view')
    print(user)
    return render(request, 'systemadmin/profile.html', {'profile': user})
