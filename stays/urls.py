from django.urls  import path
from stays.views import StayDetailView, StayListView, HostingView

urlpatterns = [
    path('' , StayListView.as_view()),
    path('/<int:stay_id>' ,StayDetailView.as_view()),
    path('/hosting' , HostingView.as_view())
]

