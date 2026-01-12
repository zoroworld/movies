from cities_light.forms import Region
from django.contrib.auth.models import User
import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from bookings.models import Booking
from movies.models import Movie
from django.db import transaction
from theatres.models import Theatre, Location, Show, ShowSeat
from django.db.models import Q
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout

# for pdf
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

# for pay

import razorpay
from django.conf import settings
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

# Initialize client
client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


# Create your views here.
def index(request):
    locations = Location.objects.all()

    data = {}

    for loc in locations:

        country_id = loc.country.id
        state_id = loc.state.id

        # Create country entry
        if country_id not in data:
            data[country_id] = {
                "name": loc.country.name,
                "states": {}
            }

        # Add state (avoid duplicates)
        data[country_id]["states"][state_id] = loc.state.name

    if request.method == "POST":
        country_id = request.POST.get("country")
        state_id = request.POST.get("state")
        return redirect('theatres-booking-details', country_id, state_id)

    return render(request, 'bookings/index.html', {
        'locations': data
    })


def book_details(request, country_id, state_id):
    if request.method == "POST":
        theatre_id = request.POST.get("theatre_id")
        return redirect('theatres-movies-view', id=theatre_id)

    locations = Location.objects.filter(
        country=country_id,
        state=state_id,
    )

    theatres = Theatre.objects.filter(location__in=locations)

    return render(request, 'bookings/book_details.html', {'theatres': theatres})


def book_start(request, movie_id, theatre_id):
    movie = Movie.objects.get(id=movie_id)
    theatre = Theatre.objects.get(id=theatre_id)

    # Get the show
    show = Show.objects.filter(movie=movie_id, theatre=theatre_id).first()
    if not show:
        return HttpResponse("No show found for this movie and theatre")

    # Create show seats for this show if missing
    show_seats_data = []

    for seat in theatre.seats.all():
        show_seat, created = ShowSeat.objects.get_or_create(
            show=show,
            seat=seat
        )
        show_seats_data.append(show_seat.seat)

    # print(show_seats_data)

    # manully show_time
    show_time = ['10:00', '12:00' , '2:00' , '4:00', '8:00', '10:00']


    # Prepare theatre seats with availability for this show
    theatre_seats = []
    for seat in theatre.seats.all():
        show_seat = ShowSeat.objects.filter(show=show, seat=seat).first()
        is_available = show_seat.is_available if show_seat else True
        theatre_seats.append({
            'seat': seat,
            'is_available': is_available,
        })



    # print(theatre_seats)

    if request.method == "POST":
        user = request.user
        seats_booked = request.POST.getlist("seats_booked")

        if not seats_booked:
            return render(request, 'bookings/book_movies.html', {
                'movie': movie,
                'theatre': theatre,
                'show': show,
                'theatre_seats': theatre_seats,
                'show_time': show_time,
                'error': "No seats selected!"
            })

        # Check all seats first for availability
        requested_show_seats = ShowSeat.objects.filter(show=show, seat_id__in=seats_booked)
        unavailable_seats = [ss.seat.seat for ss in requested_show_seats if not ss.is_available]

        if unavailable_seats:
            return render(request, 'bookings/book_movies.html', {
                'movie': movie,
                'theatre': theatre,
                'show': show,
                'show_time': show_time,
                'theatre_seats': theatre_seats,
                'error': f"These seats are already booked: {', '.join(map(str, unavailable_seats))}"
            })

        # Book seats
        with transaction.atomic():
            booking = Booking.objects.create(
                movies=movie,
                theater=theatre.name,
                user=user,
                address=f"{theatre.location}",
            )

            total_price = 0
            booked_list = []

            for show_seat in requested_show_seats:
                show_seat.is_available = False
                show_seat.save()

                booking.seats.add(show_seat.seat)
                total_price += show_seat.seat.price
                booked_list.append(str(show_seat.seat.seat))

            booking.total_price = total_price
            booking.show = show
            booking.save()

            # Store info in session
            request.session['booking_id'] = booking.id
            request.session['seats_booked'] = booked_list  # store as list

            # Redirect to payment page
            return redirect('theatres-booking-payment')

    return render(request, 'bookings/book_movies.html', {
        'movie': movie,
        'theatre': theatre,
        'show': show,
        'show_time': show_time,
        'theatre_seats': theatre_seats
    })


def book_payment(request):
    # Safely get session data
    book_id = request.session.get('booking_id')
    seats_booked = request.session.get('seats_booked', [])

    if not book_id:
        # No booking found, redirect to booking page
        return redirect('booking_page')

    # Get booking object
    booking_get = Booking.objects.get(id=book_id)

    user_name = booking_get.user.username
    user_contact = booking_get.user.contact
    amount = int(booking_get.total_price * 100)  # convert to paise
    currency = "INR"

    # Create Razorpay order
    razorpay_order = client.order.create({
        'amount': amount,
        'currency': currency,
        'payment_capture': '1',  # auto-capture
        'notes': {
            'booking_id': str(book_id),  # IMPORTANT
        }
    })
    order_id = razorpay_order['id']

    context = {
        'booking': booking_get,
        'seats_booked': seats_booked,  # pass seat list
        'order_id': order_id,
        'amount': amount,
        'currency': currency,
        'razorpay_key_id': settings.RAZORPAY_KEY_ID,
        'user_name': user_name,
        'user_contact': user_contact
    }

    return render(request, 'bookings/payment.html', context)


@csrf_exempt
def payment_success(request):
    if request.method == "POST":

        payment_id = request.POST.get('razorpay_payment_id')
        order_id = request.POST.get('razorpay_order_id')
        signature = request.POST.get('razorpay_signature')

        params_dict = {
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }

        try:
            # Verify payment signature
            client.utility.verify_payment_signature(params_dict)

            # Fetch order details from Razorpay
            razorpay_order = client.order.fetch(order_id)

            booking_id = razorpay_order['notes']['booking_id']

            booking = Booking.objects.get(id=booking_id)
            booking.status = True
            booking.save()

            user_name = booking.user.username
            user_contact = booking.user.contact
            theatre_name = booking.theater
            theatre_address = booking.address
            total_price = booking.total_price
            show = booking.show
            seats = list(booking.seats.values_list('seat', flat=True))
            # print(seats)

            context = {
                'status': True,
                'message': "Payment Successful!",
                'payment_id': payment_id,
                'booking': booking,
                'user': user_name,
                'contact': user_contact,
                'seats': seats,
                'show_date': show.date,
                'show_start_time': show.start_time,
                'show_end_time': show.end_time,
                'theatre': theatre_name,
                'theatre_address': theatre_address,
                'total_price': total_price,
                'movie': show.movie,
            }

            return render(request, 'bookings/payment_success.html', context)

        except razorpay.errors.SignatureVerificationError:
            context = {
                'status': False,
                'message': "Payment Failed!",
            }
            return render(request, 'bookings/payment_success.html', context)

    # For invalid methods
    return render(request, 'payment/failed.html', {
        'status': False,
        'message': "Invalid request!"
    })



def genrate_booking_pdf(request, id):
    booking = get_object_or_404(Booking, id=id)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="booking_{booking.id}.pdf"'

    doc = SimpleDocTemplate(response, pagesize=A4)
    elements = []
    styles = getSampleStyleSheet()
    h1 = styles['Heading1']
    h3 = styles['Heading3']
    p = styles['BodyText']

    # ---- TITLE ----
    elements.append(Paragraph("🎟️ Movie Ticket Confirmation", h1))
    elements.append(Spacer(1, 16))

    # ---- BOOKING INFO ----

    seats = list(booking.seats.values_list('seat', flat=True))
    seat_string = ", ".join(map(str, seats))  # FIX HERE

    info = [
        ["Booking ID:", str(booking.id)],
        ["Movie Name:", booking.show.movie.title],
        ["Theatre:", booking.show.theatre.name],
        ["Address:", booking.address],
        ["Show Date:", booking.show.date.strftime("%b %d, %Y")],
        ["Start Time:", booking.show.start_time.strftime("%I:%M %p")],
        ["End Time:", booking.show.end_time.strftime("%I:%M %p")],
        ["Seats:", seat_string],  # <<< FIX HERE
        ["Total Price:", f"Rs {booking.total_price}"],
    ]

    table = Table(info, colWidths=[130, 350])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 0.3, colors.grey),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 20))

    # ---- USER DETAILS ----
    elements.append(Paragraph("User Details", h3))

    user_table = Table([
        ["User:", booking.user.username],
        ["Contact:", booking.user.contact],
    ], colWidths=[130, 350])

    user_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 0.3, colors.grey),
    ]))

    elements.append(user_table)
    elements.append(Spacer(1, 30))

    # ---- FOOTER ----
    elements.append(Paragraph(
        "Thank you for booking with ShowField Theater!<br/>Enjoy your show 🍿",
        p
    ))

    doc.build(elements)
    return response
