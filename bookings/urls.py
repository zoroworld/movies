from django.urls import path, include
from .views import index, book_details, book_start, book_payment, genrate_booking_pdf, payment_success

urlpatterns = [
    path('', index, name='booking-view'),
    path('country/<int:country_id>/state/<int:state_id>', book_details, name='theatres-booking-details'),
    path('movies/<int:movie_id>/theatre/<int:theatre_id>', book_start, name='theatres-movies-seats-booking'),
    path('payment', book_payment, name='theatres-booking-payment'),
    path('payment/success', payment_success, name='payment-success'),
    path('payment-pdf/<int:id>', genrate_booking_pdf, name='genrate_booking_pdf'),
]
