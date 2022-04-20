import jwt, unittest

from unittest.mock import patch, MagicMock

from django.test import TestCase, Client
from django.conf import settings
from django.http import JsonResponse

from users.views import KakaoClient

client = Client()

class KakaoLoginTest(TestCase):
    @patch('users.views.requests')
    def test_kakao_auth_code_invalid(self,mocked_token):
        class mocked_kakao_auth_url_requests:
            def __init__(self):
                self.status_code = 400

            def json(self):
                return {'no_token' : 'no_token'}
        
        mocked_token.post.return_value = mocked_kakao_auth_url_requests()

        response = client.post('/users/signin')

        self.assertEqual(response.status_code , 400)
        self.assertEqual(eval(response.content.decode('utf-8'))['message'] , "AUTH_CODE_INVALID_ERROR")

    @patch('users.views.requests')
    def test_kakao_token_invalid(self,mocked_user_data):
        class mocked_kakao_api_url_requests:
            def __init__(self):
                self.status_code = 401

            def json(self):
                return {'access_token' : 'invalid_token'}

        mocked_user_data.post.return_value = mocked_kakao_api_url_requests()

        response = client.post('/users/signin')
        
        self.assertEqual(response.status_code , 401)
        self.assertEqual(eval(response.content.decode('utf-8'))['message'] , 'ACCESS_TOKEN_INVALID_ERROR')

    @patch.object(KakaoClient, "get_user_info")
    @patch.object(KakaoClient, "get_access_token")
    def test_kakao_signin_new_user_success(self, mocked_token, mocked_user_data):
        MockedToken = {"access_token" : "1234"}
        MockedUserData = {
            'id' : 22,
            'kakao_account' : {
                'email' : 123,
                'birthday' : 123,
                'age_range' : '20~29'
            },
            'properties' : {
                'nickname' : 123
            }
        }
        mocked_token.return_value     = MockedToken
        mocked_user_data.return_value = MockedUserData

        response = client.post('/users/signin')
        payload  = jwt.decode(response.json()['token'], settings.SECRET_KEY, algorithms=settings.ALGORITHM)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(payload['user_id'],2)