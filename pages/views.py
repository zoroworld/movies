from django.contrib.auth.middleware import get_user
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from systemadmin.models import NewUser
from movies.models import Movie
from theatres.models import Seat
from django.core.paginator import Paginator
from django.db.models import Q
from bookings.models import Booking
# Create your views here.
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout


def home(request):
    movies = Movie.objects.all().order_by('-id')[:4]
    genres = []
    for genre in Movie.objects.values_list('genre', flat=True).distinct():
        poster = Movie.objects.filter(genre=genre).first().poster
        genres.append([genre, poster])

    return render(request, 'pages/home.html', {'movies': movies, 'genres': genres})


def about(request):
    return render(request, 'pages/about.html')


from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from movies.models import Movie
from theatres.models import Theatre


def movies(request, theatre_id=None):
    user = request.user

    # If user not logged in
    if not user.is_authenticated:
        return render(request, "movies/movies.html")

    # Get theatre only if page requires it
    theatre = None
    if theatre_id:
        theatre = get_object_or_404(Theatre, id=theatre_id)

    # Filters
    search = request.GET.get("search", "")
    language = request.GET.get("language", "")
    genre = request.GET.get("genre", "")
    year = request.GET.get("year", "")

    # Base queryset
    movies = Movie.objects.all()

    # If theatre is provided → filter theatre movies only
    if theatre:
        movies = movies.filter(theatres=theatre)

    # Search
    if search:
        movies = movies.filter(
            Q(title__icontains=search) | Q(description__icontains=search)
        )

    # Filters
    if language:
        movies = movies.filter(language__icontains=language)

    if genre:
        movies = movies.filter(genre__icontains=genre)

    if year:
        movies = movies.filter(release_date__year=year)

    # Pagination
    paginator = Paginator(movies, 8)
    page_number = request.GET.get("page")
    movies_page = paginator.get_page(page_number)

    # Only normal users can see movies
    if user.is_admin == 0:
        return render(request, "movies/movies.html", {
            "movies": movies_page,
            "theatre": theatre,
            "search": search,
            "language": language,
            "genre": genre,
            "year": year,
        })
    else:
        return render(request, "movies/movies.html")


def movies_by_genre(request, genre):
    movies = Movie.objects.filter(genre__iexact=genre)
    return render(request, 'movies/movies_by_genre.html', {'movies': movies, 'genre': genre})


def movie_detail(request, id):
    if request.method == 'GET':
        movie = get_object_or_404(Movie, id=id)
        return render(request, 'movies/movie_detail.html', {'movie': movie})

    if request.method == 'POST':
        user = request.user
        seats_booked = request.POST.get('seats_booked', '')  # e.g. "21,22,25"
        seat_ids = [int(s) for s in seats_booked.split(',') if s.strip()]  # list of ints

        seats = Seat.objects.filter(id__in=seat_ids)
        for seat in seats:
            if not seat.is_available:
                return redirect('movies')

        # Store temporary booking data in session or pass via payment gateway metadata
        request.session['booking_data'] = {
            'movie_id': id,
            'seat_ids': seat_ids
        }

        # Redirect to payment page (Razorpay / Stripe, etc.)
        return redirect('payment')


def booking(request):
    return render(request, 'pages/movies.html')


def contact(request):
    return render(request, 'pages/contact.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)  # Start user session

            if user.is_admin:
                return redirect('dashboard-view')  # Use a named URL instead of template path
            else:
                return redirect('movies')
        else:
            return render(request, 'pages/login.html', {'error': 'Invalid username or password'})

    return render(request, 'pages/login.html')


def signup(request):
    if request.method == 'POST':
        users = NewUser.objects.all()
        profile_pic = request.FILES.get('profile_pic')
        if profile_pic:
            profile_pic = profile_pic  # Save uploaded file
        else:
            profile_pic = 'default/default.jpg'
        username = request.POST['username']
        password = request.POST['password']
        confirmPassword = request.POST['confirmpassword']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        email = request.POST['email']
        contact = request.POST['contact']
        if (password != confirmPassword):
            return render(request, 'pages/login.html', {'password_error': 'Passwords do not match'})

        for user in users:
            if user.username == username:
                return render(request, 'pages/signup.html', {'username_error': 'Username already taken'})

            if user.email == email:
                return render(request, 'pages/signup.html', {'email_error': 'Email already taken'})

        createUser = NewUser.objects.create(profile_pic=profile_pic, username=username, first_name=first_name,
                                            last_name=last_name, email=email, contact=contact)
        createUser.set_password(password)
        createUser.save()
    return render(request, 'pages/signup.html')


def logout(request):
    user = request.user

    # Log the user out (clears session)
    auth_logout(request)

    # Redirect based on role
    if hasattr(user, 'is_admin') and user.is_admin:
        return redirect('login')
    else:
        return redirect('login')
