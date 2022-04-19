import json
import uuid , boto3

from django.http    import JsonResponse
from django.views   import View


from staies.models  import *
from users.models   import *
from cores.utils    import author

class StayDetailView(View):
    def get(self, request, stay_id):
        try:
            stay        = Stay.objects.get(id = stay_id)
            images      = StayImage.objects.filter(stay = stay_id)
            services    = Service.objects.filter(stayservice__stay_id = stay_id)
            amenities   = Amenity.objects.filter(stayamenity__stay_id = stay_id)
            highlights  = Highlight.objects.filter(stayhighlight__stay_id = stay_id)
            
            result = {
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
        
class HostingView(View):
    s3_client = boto3.client(
                's3',
                aws_access_key_id = settings.AWS_ACCESS_KEY_ID , 
                aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY
    )
    @author
    def post(self, request):
        try:
            user = request.user
            images = request.FILES.getlist('image')
            User.objects.get(id=user.id).update(is_host=True)

            new_stay = Stay.objects.create(
                user_id         = user.id,
                title           = request.POST['title'],
                price           = request.POST['price'],
                bed             = request.POST['bed'],
                bedroom         = request.POST['bedRoom'],
                bathroom        = request.POST['bathRoom'],
                guest_adult     = request.POST['maxAdult'],
                guest_kid       = request.POST['maxKid'],
                guest_pet       = request.POST['maxPet'],
                stay_type_id    = request.POST['stayTypeID'],
                description     = request.POST['description'],
                address         = request.POST['address'],
                latitude        = request.POST['latitude'],
                longitude       = request.POST['longitude']
            )

            if len(images) < 2:
                return JsonResponse({"message" : "2장 이상의 이미지가 필요합니다."}, status=400)

            for image in images:
                dolharu_uuid = str(uuid.uuid4())
                self.s3_client.upload_fileobj(
                    image,
                    "dolharu", 
                    f'dolharu_images/{dolharu_uuid}',        
                )
                image_url = "https://dolharu.s3.ap-northeast-2.amazonaws.com/dolharu_images/" + dolharu_uuid
                
                StayImage.objects.create(
                    image_url = image_url,
                    stay_id   = new_stay.id
                )
            
            [StayService.objects.create(stay_id = new_stay.id , service_id = service_id) for service_id in request.POST.getlist('services')]
            
            [StayAmenity.objects.create(stay_id = new_stay.id, amenity_id = amenity_id) for amenity_id in request.POST.getlist('amenities')]
            
            [StayHighlight.objects.create(stay_id = new_stay.id, highlight_id =highlight_id) for highlight_id in request.POST.getlist('highlights')]
            
            return JsonResponse({'message' : 'SUCCESS'} , status = 200)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'} , status = 402)