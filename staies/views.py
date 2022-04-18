from django.http    import JsonResponse
from django.views   import View

from staies.models  import *
from users.models   import *

class StayDetailView(View):
    def get(self, request, stay_id):
        try:
            stay        = Stay.objects.get(id = stay_id)
            images      = StayImage.objects.filter(stay = stay_id)
            services    = Service.objects.filter(stayservice__stay_id = stay_id)
            amenities   = Amenity.objects.filter(stayamenity__stay_id = stay_id)
            highlights  = Highlight.objects.filter(stayhighlight__stay_id = stay_id)
            
            result = {
                'stayHost'      : stay.user.nick_name,
                'stayId'        : stay.id,
                'title'         : stay.title,
                'price'         : stay.price,
                'description'   : stay.description,
                'placeImages'   : [ image.image_url for image in images],
                'bed'           : stay.bed,
                'bedRoom'       : stay.bedroom,
                'bathRoom'      : stay.bathroom,
                'maxAdult'      : stay.guest_adult,
                'maxKid'        : stay.guest_kid,
                'maxPet'        : stay.guest_pet,
                'stayType'      : StayType.objects.get(stay = stay_id).name,
                'address'       : stay.address,
                'latitude'      : stay.latitude,
                'longitude'     : stay.longitude,
                'services'      : [ service.name for service in services ],
                'amenities'     : [ amenity.name for amenity in amenities],
                'highlights'    : [ highlight.name for highlight in highlights]
            }
            
            return JsonResponse({'result' : result} , status = 200)
        except Stay.DoesNotExist:
            return JsonResponse({'message' : 'STAY_DOES_NOT_EXIST'} , status = 404)
