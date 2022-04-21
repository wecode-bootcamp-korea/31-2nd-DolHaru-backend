import re
import uuid , boto3


from django.http    import JsonResponse
from django.views   import View
from django.db      import transaction

from django.conf    import settings
from cores.utils    import author
from stays.models   import *
from users.models   import *

class StayListView(View):
    def get(self,request):
        self.offset   = int(request.GET.get('offset' , 0))
        self.limit    = int(request.GET.get('limit' , 12))

        filter_option    = request.GET
        filters          = self.create_filters(filter_option)
        stays_filtered   = self.filter_stays(filters)
        stay_list_detail = self.return_stay_list_detail(stays_filtered)

        return JsonResponse({'stay_list' : stay_list_detail} , status=200)

    def create_filters(self,filter_option):
        FILTER_SET = {
            'price_min' : 'price__gte',
            'price_max' : 'price__lte',
            'stay_type' : 'stay_type__id',
            'amenity'   : 'amenities__id',
            'service'   : 'services__id',
            'highlight' : 'highlight__id',
        }        
        filters = {FILTER_SET[key]:value for key,value in filter_option.items() if FILTER_SET.get(key)} 

        return filters

    def filter_stays(self,filters):
        stays_filtered = Stay.objects.filter(**filters).prefetch_related('stayimage_set','stayservice_set__service')[self.offset:self.offset+self.limit]

        return stays_filtered

    def return_stay_list_detail(self,stays_query_optimization):
        stay_list_detail = [{
            'stayId'      : stay.id,
            'placeImages' : [stayimage.image_url for stayimage in stay.stayimage_set.all()],
            'description' : stay.description,
            'placeName'   : stay.title,
            'adult'       : stay.guest_adult,
            'kid'         : stay.guest_kid,
            'pet'         : stay.guest_pet,
            'bed'         : stay.bed,
            'bedRoom'     : stay.bedroom,
            'bathRoom'    : stay.bathroom,
            'stayService' : [service.service.name for service in stay.stayservice_set.all()],
            'price'       : stay.price
        } for stay in stays_query_optimization]

        return stay_list_detail

class StayDetailView(View):
    def get(self, request, stay_id):
        try:
            stay = Stay.objects.select_related('user', 'stay_type')\
                .prefetch_related('services', 'amenities', 'highlight')\
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
                'services'      : [service.name for service in stay.services.all()],
                'amenities'     : [amenity.name for amenity in stay.amenities.all()],
                'highlights'    : [highlight.name for highlight in stay.highlight.all()]
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
    def image_upload(self, image):
        dolharu_uuid = str(uuid.uuid4())
        self.s3_client.upload_fileobj(
            image,
            "dolharu", 
            f'dolharu_images/{dolharu_uuid}'
        )

        self.image_uuid = dolharu_uuid
        return self.image_uuid

    @author
    def post(self, request):
        try:
            user   = request.user
            images = request.FILES.getlist('image')
            data   = request.POST
            
            if len(images) < 2:
                    return JsonResponse({"message" : "2장 이상의 이미지가 필요합니다."}, status=400)

            print(data)

            with transaction.atomic():   
                new_stay = Stay.objects.create(
                    user_id         = user.id,
                    title           = data['title'],
                    price           = data['price'],
                    bed             = data['bed'],
                    bedroom         = data['bedroom'],
                    bathroom        = data['bathroom'],
                    guest_adult     = data.get('maxAdult', 0),
                    guest_kid       = data.get('maxKid', 0),
                    guest_pet       = data.get('maxPet', 0),
                    stay_type_id    = data['stayTypeID'],
                    description     = data['description'],
                    address         = data['address'],
                    latitude        = data['latitude'],
                    longitude       = data['longitude']
                )    
                
                user.is_host=True
                
                stay_sevice_list    = [StayService(stay_id = new_stay.id, service_id = service_id) for service_id in data.getlist('services')]
                StayService.objects.bulk_create(stay_sevice_list)
                
                stay_amenity_list   = [StayAmenity(stay_id = new_stay.id, amenity_id = amenity_id) for amenity_id in data.getlist('amenities')]
                StayAmenity.objects.bulk_create(stay_amenity_list)
                    
                stay_highlight_list = [StayHighlight(stay_id = new_stay.id, highlight_id =highlight_id) for highlight_id in data.getlist('highlights')]
                StayHighlight.objects.bulk_create(stay_highlight_list)
                
                for image in images:
                    image_url   = self.image_upload(image)
                    StayImage.objects.create(image_url = image_url, stay_id = new_stay.id)

            return JsonResponse({'message' : 'SUCCESS'} , status = 200)
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'} , status = 400)
