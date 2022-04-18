import requests, json, jwt

from django.http  import JsonResponse
from django.views import View
from django.conf  import settings
from datetime     import datetime, timedelta

from users.models import User

class KakaoClient:
    def __init__(self):
        self.kakao_auth_url = "https://kauth.kakao.com"
        self.kakao_api_url  = "https://kapi.kakao.com"

    def get_access_token(self, auth_code):
        auth_code_url = f"{self.kakao_auth_url}/oauth/token"
        data = {
            "grant_type": "authorization_code",
            "client_id" : settings.REST_API_KEY,
            "code"      : auth_code
        }
        print('befor_requests_mock')
        token_data = requests.post(auth_code_url , data = data , timeout = 2)

        if token_data.status_code == 400:
            raise Exception('AUTH_CODE_INVALID_ERROR' , 400)
        
        return token_data.json()
        
    def get_user_info(self, access_token):
        token_url = f"{self.kakao_api_url}/v2/user/me"
        
        user_info = requests.post(token_url, headers = {"Authorization" : f"Bearer {access_token}"} , timeout = 2)
        
        if user_info.status_code == 401:
            raise Exception('ACCESS_TOKEN_INVALID_ERROR' , 401)

        return user_info.json()
    
class KakaoSignInView(View):
    def post(self,request):
        try:
            auth_code  = request.GET.get('code') 
            client     = KakaoClient()
            
            token_data   = client.get_access_token(auth_code)
            access_token = token_data['access_token']
            user_info    = client.get_user_info(access_token)

            user      = self.get_or_create(user_info)
            token     = self.create_token(user.id)

            return JsonResponse({'token' : token}, status = 200)
        except Exception as e:
            return JsonResponse({'message' : e.args[0]} , status = e.args[1])
        
    def get_or_create(self, user_info):
        user , is_created = User.objects.get_or_create(
            kakao_id   = user_info['id'],
            defaults = {
                'is_host'    : False,
                'email'      : user_info['kakao_account']['email'],
                'nick_name'  : user_info['properties']['nickname'],
                'birth_date' : user_info['kakao_account']['birthday'],
                'is_adult'   : int(user_info['kakao_account']['age_range'][0]) > 1
            }
        )
        if not is_created:
            user.email      = user_info['kakao_account']['email']
            user.nick_name  = user_info['properties']['nickname']
            user.birth_date = user_info['kakao_account']['birthday']
            user.is_adult   = int(user_info['kakao_account']['age_range'][0]) > 1
            user.save()

        return user

    def create_token(self, user_id):
        token = jwt.encode({'user_id' : user_id , 'exp':datetime.utcnow() + timedelta(days = 3)}, settings.SECRET_KEY, settings.ALGORITHM)

        return token