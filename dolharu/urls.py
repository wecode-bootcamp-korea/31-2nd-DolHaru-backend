from django.urls import path, include

urlpatterns = [
    path('staies', include('staies.urls')),
    path('users', include('users.urls')),
    path('bookings', include('bookings.urls'))
]