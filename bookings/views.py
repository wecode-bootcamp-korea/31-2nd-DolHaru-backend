from django.http import JsonResponse

from django.db    import transaction
from django.views import View
from cores.utils  import author
from bookings.models import Booking, Status
# Create your views here.


class BookingView(View):
    @author
    def get(self, request):
        user    = request.user
        booking_list = Booking.objects.filter(user_id = user.id)
 
        list = [{
            'checkIn' : booking.check_in,
            'price'   : booking.price,
            'adult'   : booking.adult,
            'children': booking.children,
            'pet'     : booking.pet,
            'status'  : booking.status.name,
            'user'    : user.id,
            'stay'    : booking.stay.id
        } for booking in booking_list]
   
        return JsonResponse({'result' : list}, status = 200)
    
    @author
    def post(self, request):
        try:
            user = request.user
            data = request.POST

            new_booking = Booking.objects.create(
                check_in    = data['checkIn'],
                price       = data['price'],
                adult       = data['adult'],
                children    = data['children'],
                pet         = data['pet'],
                status      = data['status'],
                user        = user.id,
                stay        = data['stay']
            )
            return JsonResponse({'message' : 'success', 'new_booking' : new_booking}, status = 200)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status = 400)
            