from django.urls  import path
from bookings.views import BookingView

urlpatterns = [
    path('/book' ,BookingView.as_view())
]