from django.urls import path, include
from .views import admin, movies, users, booking_history, create_movies, edit_movies, delete_movies, theaters, \
    create_theaters, edit_theaters, delete_theaters, load_states, load_cities, create_show,get_profile, edit_users, delete_users

urlpatterns = [
    path('', admin, name='dashboard-view'),
    path('movies/', include([
        path('view/', movies, name='dashboard-movies-view'),
        path('create/', create_movies, name='dashboard-movies-create'),
        path('edit/<int:id>', edit_movies, name='dashboard-movies-edit'),
        path('delete/<int:id>', delete_movies, name='dashboard-movies-delete')
    ])),
    path('theaters/', include([
        path('view/', theaters, name='dashboard-theaters-view'),
        path('create/', create_theaters, name='dashboard-theaters-create'),
        path('edit/<int:id>', edit_theaters, name='dashboard-theaters-edit'),
        path('delete/<int:id>', delete_theaters, name='dashboard-theaters-delete'),
        path('ajax/load-states/', load_states, name='ajax_load_states'),
        path('ajax/load-cities/', load_cities, name='ajax_load_cities'),
    ])),

    path('shows/', include([
        path('create/', create_show, name='create_show'),
    ])),

    path('users/', include([
        path('view/', users, name='dashboard-user-view'),
        path('edit/<int:id>', edit_users, name='dashboard-user-edit'),
        path('delete/<int:id>', delete_users, name='dashboard-user-delete'),
    ])),
    path('profile/', include([
        path('<int:id>', get_profile, name='dashboard-user-profile-view'),
    ])),

    path('booking-history', booking_history, name='dashboard-booking-history'),
]
