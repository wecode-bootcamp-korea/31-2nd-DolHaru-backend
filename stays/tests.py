from django.test    import TestCase , Client
from stays.models  import *
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

        StayType.objects.create(
            id              = 2,
            name            = '빌라'
        )

        StayType.objects.create(
            id              = 3,
            name            = '풀빌라'
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

        Highlight.objects.create(
            id              = 2,
            name            = '넓은 공간'
        )
        
        
        stays = [Stay(
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
            latitude        = 11.0000011111222,
            longitude       = 11.0000011111222,
        ),
        Stay(
            id              = 2,
            user_id         = 1,
            title           = '행복여행 제주도 훈이네',
            price           = '20000.00',
            bed             = 2,
            bedroom         = 2,
            bathroom        = 2,
            guest_adult     = 2,
            guest_kid       = 2,
            guest_pet       = 2,
            stay_type_id    = 1,
            description     = '모두가 행복해지는 숙소',
            address         = '제주도 어딘가',
            latitude        = 11.0000011111222,
            longitude       = 11.0000011111222,
        ),
        Stay(
            id              = 3,
            user_id         = 1,
            title           = '행복여행 제주도 훈이네',
            price           = '30000.00',
            bed             = 2,
            bedroom         = 2,
            bathroom        = 2,
            guest_adult     = 2,
            guest_kid       = 2,
            guest_pet       = 2,
            stay_type_id    = 2,
            description     = '모두가 행복해지는 숙소',
            address         = '제주도 어딘가',
            latitude        = 11.0000011111222,
            longitude       = 11.0000011111222,
        ),
        Stay(
            id              = 4,
            user_id         = 1,
            title           = '행복여행 제주도 훈이네',
            price           = '40000.00',
            bed             = 2,
            bedroom         = 2,
            bathroom        = 2,
            guest_adult     = 2,
            guest_kid       = 2,
            guest_pet       = 2,
            stay_type_id    = 2,
            description     = '모두가 행복해지는 숙소',
            address         = '제주도 어딘가',
            latitude        = 11.0000011111222,
            longitude       = 11.0000011111222,
        ),
        Stay(
            id              = 5,
            user_id         = 1,
            title           = '행복여행 제주도 훈이네',
            price           = '50000.00',
            bed             = 2,
            bedroom         = 2,
            bathroom        = 2,
            guest_adult     = 2,
            guest_kid       = 2,
            guest_pet       = 2,
            stay_type_id    = 3,
            description     = '모두가 행복해지는 숙소',
            address         = '제주도 어딘가',
            latitude        = 11.0000011111222,
            longitude       = 11.0000011111222,
        ),
        Stay(
            id              = 6,
            user_id         = 1,
            title           = '행복여행 제주도 훈이네',
            price           = '60000.00',
            bed             = 2,
            bedroom         = 2,
            bathroom        = 2,
            guest_adult     = 2,
            guest_kid       = 2,
            guest_pet       = 2,
            stay_type_id    = 3,
            description     = '모두가 행복해지는 숙소',
            address         = '제주도 어딘가',
            latitude        = 11.0000011111222,
            longitude       = 11.0000011111222,
        )
        ]
        Stay.objects.bulk_create(stays)
        
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
        
        StayService.objects.create(
            id              = 4,
            service_id      = 3,
            stay_id         = 2,
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
        response = client.get("/stays/1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"result": {
        "stayId": 1,
        "hostName" : "successboy",
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
        "latitude": "11.0000011111222",
        "longitude": "11.0000011111222",
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
        response = client.get("/stays/50000")
        self.assertEqual(response.status_code, 404)

    def test_stay_list_all(self):
        response = client.get("/stays")
        self.assertEqual(len(response.json()["stay_list"]), 6)

    def test_stay_list_offset_limit(self):
        response = client.get("/stays?offset=3&limit=2")
        self.assertEqual(len(response.json()["stay_list"]), 2)

    def test_stay_list_price_min(self):
        response = client.get("/stays?price_min=35000")
        self.assertEqual(len(response.json()["stay_list"]), 4)    

    def test_stay_list_price_max(self):
        response = client.get("/stays?price_max=45000")
        self.assertEqual(len(response.json()["stay_list"]), 3)
    
    def test_stay_list_stay_type(self):
        response = client.get("/stays?stay_type=1")
        self.assertEqual(len(response.json()["stay_list"]), 2)

    def test_stay_list_amenity(self):
        response = client.get("/stays?amenity=1&amenity=2")
        self.assertEqual(len(response.json()["stay_list"]), 1)
    
    def test_stay_list_service(self):
        response = client.get("/stays?service=1&service=2&service=3")
        self.assertEqual(len(response.json()["stay_list"]), 2)

    def test_stay_list_highlight(self):
        response = client.get("/stays?highlight=1")
        self.assertEqual(len(response.json()["stay_list"]), 1)