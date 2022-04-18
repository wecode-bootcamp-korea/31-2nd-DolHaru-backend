import jwt

from unittest.mock import patch, MagicMock

from django.test import TestCase, Client
from django.conf import settings

from users.views import KakaoClient

client = Client()
class KakaoLoginTest(TestCase):
    @patch.object(KakaoClient, "request_access_token")
    def test_kakao_auth_code_invalid(self, mocked_token):
        class MockedToken:
            def json(self):
                return {"no_access_token" : "no_access_token"}
        
        mocked_token.return_value = MockedToken().json()

        response = client.post('/users/signin')

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json(), {'message' : 'KEY_ERROR'})

    @patch.object(KakaoClient, "request_user_data")
    def test_kakao_token_invalid(self,mocked_user_data):
        class MockedUserData:
            def json(self):
                return {"no_user_data" : "no_user_data"}
        
        mocked_user_data = MockedUserData().json()

        response = client.post('/users/signin')

        self.assertEqual(response.status_code,400)
        self.assertEqual(response.json(), {'message' : 'KEY_ERROR'})

    @patch.object(KakaoClient, "request_user_data")
    @patch.object(KakaoClient, "request_access_token")
    def test_kakao_signin_new_user_success(self, mocked_token, mocked_user_data):
        class MockedToken:
            def json(self):
                return {"access_token" : "1234"}
        class MockedUserData:
            def json(self):
                return {
                    'id' : 12,
                    'kakao_account' : {
                        'email' : 123,
                        'birthday' : 123,
                        'age_range' : '20~29'
                    },
                    'properties' : {
                        'nickname' : 123
                    }
                }
        mocked_token.return_value     = MockedToken().json()
        mocked_user_data.return_value = MockedUserData().json()

        response = client.post('/users/signin')
        payload  = jwt.decode(response.json()['token'], settings.SECRET_KEY, algorithms=settings.ALGORITHM)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(payload['user_id'],1)