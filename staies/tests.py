from django.test    import TestCase , Client
from staies.models  import *
from users.models   import User

client = Client()

class StayDetailPageTest(TestCase):
    def setUp(self):
        User.objects.create(
            id          = 1,
            kakao_id    = 1,
            is_host     = False,
            is_adult    = True,
            email       = 'plz8282@success.com',
            nick_name   = 'successboy',
            birth_date  = '2000-01-01'
        )
        
        StayType.objects.create(
            id              = 1,
            name            = '호텔'
        )
        
        Service.objects.create(
            id              = 1,
            name            = '조식'
        )
        
        Service.objects.create(
            id              = 2,
            name            = '일식'
        )
        
        Service.objects.create(
            id              = 3,
            name            = '양식'
        )
        
        Amenity.objects.create(
            id              = 1,
            name            = 'wifi'
        )
        
        Amenity.objects.create(
            id              = 2,
            name            = '드라이기'
        )
        
        Amenity.objects.create(
            id              = 3,
            name            = '커피포트'
        )
        
        Highlight.objects.create(
            id              = 1,
            name            = '스타일리쉬'
        )
        
        
        Stay.objects.create(
            id              = 1,
            user_id         = 1,
            title           = '행복여행 제주도 훈이네',
            price           = '80000.00',
            bed             = 2,
            bedroom         = 2,
            bathroom        = 2,
            guest_adult     = 2,
            guest_kid       = 2,
            guest_pet       = 2,
            stay_type_id    = 1,
            description     = '모두가 행복해지는 숙소',
            address         = '제주도 어딘가',
            latitude        = 11.0000001,
            longitude       = 11.0000001,
        )
        
        StayService.objects.create(
            id              = 1,
            service_id      = 1,
            stay_id         = 1,
        )
        
        StayService.objects.create(
            id              = 2,
            service_id      = 2,
            stay_id         = 1,
        )
        
        StayService.objects.create(
            id              = 3,
            service_id      = 3,
            stay_id         = 1,
        )
        
        StayAmenity.objects.create(
            id              = 1,
            amenity_id      = 1,
            stay_id         = 1,
        )
        
        StayAmenity.objects.create(
            id              = 2,
            amenity_id      = 2,
            stay_id         = 1,
        )
        
        StayAmenity.objects.create(
            id              = 3,
            amenity_id      = 3,
            stay_id         = 1,
        )
        
        StayHighlight.objects.create(
            id              = 1,
            stay_id         = 1,
            highlight_id    = 1,
        )
        
        StayImage.objects.create(
            id              = 1,
            stay_id         = 1,
            image_url       = 'happy.url'
        )
        
    def tearDown(self):
        User.objects.all().delete()
        Stay.objects.all().delete()
        StayType.objects.all().delete()
        StayImage.objects.all().delete()
        Service.objects.all().delete()
        StayService.objects.all().delete()
        Amenity.objects.all().delete()
        StayAmenity.objects.all().delete()
        Highlight.objects.all().delete()
        StayHighlight.objects.all().delete()
    
    
    def test_stay_detail_view_success(self):
        respone = client.get("/staies/1")
        self.assertEqual(respone.status_code, 200)
        self.assertEqual(respone.json(), {"result": {
        "stayId": 1,
        "title": "행복여행 제주도 훈이네",
        "price": "80000.00",
        "description": "모두가 행복해지는 숙소",
        "placeImages": [
            "happy.url"
        ],
        "bed": 2,
        "bedRoom": 2,
        "bathRoom": 2,
        "maxAdult": 2,
        "maxKid": 2,
        "maxPet": 2,
        "stayType": "호텔",
        "address": "제주도 어딘가",
        "latitude": "11.0000011111321",
        "longitude": "11.0000011111321",
        "services": [
            "조식",
            "일식",
            "양식"
        ],
        "amenities": [
            "wifi",
            "드라이기",
            "커피포트"
        ],
        "highlights": [
            "스타일리쉬",
        ]
         }})
        
    def test_stay_does_not_exist(self):
        respone = client.get("/staies/50000")
        self.assertEqual(respone.status_code, 404)