from django.http    import JsonResponse
from django.views   import View

from staies.models  import *
from users.models   import *

class StayDetailView(View):
    def get(self, request, stay_id):
        try:
            stay = Stay.objects.select_related('user', 'stay_type')\
                .prefetch_related('stayimage_set','services', 'amenities', 'highlight')\
                .get(id = stay_id)
            
            result = {
                'stayId'        : stay.id,
                'hostName'      : stay.user.nick_name,
                'title'         : stay.title,
                'price'         : stay.price,
                'description'   : stay.description,
                'placeImages'   : [image.image_url for image in stay.stayimage_set.all()],
                'bed'           : stay.bed,
                'bedRoom'       : stay.bedroom,
                'bathRoom'      : stay.bathroom,
                'maxAdult'      : stay.guest_adult,
                'maxKid'        : stay.guest_kid,
                'maxPet'        : stay.guest_pet,
                'stayType'      : stay.stay_type.name,
                'address'       : stay.address,
                'latitude'      : stay.latitude,
                'longitude'     : stay.longitude,
                'services'      : [ service.name for service in stay.services.all()],
                'amenities'     : [ amenity.name for amenity in stay.amenities.all()],
                'highlights'    : [ highlight.name for highlight in stay.highlight.all()]
            }
            return JsonResponse({'result' : result} , status = 200)
        except Stay.DoesNotExist:
            return JsonResponse({'message' : 'STAY_DOES_NOT_EXIST'} , status = 404)
