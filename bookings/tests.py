import jwt
from django.conf    import settings

from django.test    import TestCase , Client
from unittest.mock  import patch
from users.models   import User
from staies.models  import Stay, Service, Amenity, Highlight, StayType, StayImage, StayHighlight, StayService, StayAmenity
from bookings.models import Booking, Status
# Create your tests here.
client = Client()

class BookingTest(TestCase):
    def setUp(self):
        User.objects.create(
        kakao_id    = 1,
        is_host     = False,
        is_adult    = True,   
        email       = 'hotsix@gmail.com',    
        nick_name   = 'successboy',
        birth_date  = '1995-01-01'  
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
            latitude        = 11.0000011111222,
            longitude       = 11.0000011111222,
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

        Status.objects.create(
            id = 1,
            name    = '예약중'
        )

        Booking.objects.create(
                check_in    = '2021-04-21',
                price       = 2300000.00,
                adult       = 2,
                children    = 2,
                pet         = 0,
                status_id      = 1,
                user_id        = 1,
                stay_id        = 1
            )

        Booking.objects.create(
                check_in    = '2021-04-11',
                price       = 1300000.00,
                adult       = 2,
                children    = 2,
                pet         = 0,
                status_id     = 1,
                user_id        = 1,
                stay_id        = 1
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


    def test_booking_get_success(self):
        client = Client()
        test_token = jwt.encode({'user_id' : 1}, settings.SECRET_KEY, settings.ALGORITHM)

        headers = {'HTTP_Authorization': test_token, 'content-type' : 'aplication/json'}
        response = client.get('/bookings/book', **headers )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['result']), 2)
       
        

