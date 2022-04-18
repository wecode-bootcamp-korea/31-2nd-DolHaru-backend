from django.urls  import path
from staies.views import StayDetailView

urlpatterns = [
    path('/<int:stay_id>' ,StayDetailView.as_view()),
    path('/hosting' , HostingView.as_view())
]