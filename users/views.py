import requests, json, jwt

from django.http  import JsonResponse
from django.views import View
from django.conf  import settings
from datetime     import datetime, timedelta

from users.models import User

class KakaoClient(View):
    def request_access_token(self, auth_code):
        auth_code_url = "https://kauth.kakao.com/oauth/token"
        data = {
            "grant_type": "authorization_code",
            "client_id" : settings.REST_API_KEY,
            "code"      : auth_code
        }
        token_data = requests.post(auth_code_url , data = data , timeout = 2)

        return token_data
        
    def request_user_data(self, access_token):
        token_url = "https://kapi.kakao.com/v2/user/me"
        user_data = requests.post(token_url, headers = {"Authorization" : f"Bearer {access_token}"} , timeout = 2)

        return user_data
    
class KakaoSignInView(View):
    def post(self,request):
        auth_code  = request.GET.get('code')
        client     = KakaoClient()

        token_data = client.request_access_token(auth_code)

        if token_data.status_code == 400:
            return JsonResponse({'message' : 'AUTH_CODE_INVALID_ERROR'} , status = 400)
        
        access_token = token_data.json()['access_token']
        user_data    = client.request_user_data(access_token)
        
        if user_data.status_code == 401:
            return JsonResponse({'message' : 'ACCESS_TOKEN_INVALID_ERROR'} , status = 401)

        user_info = user_data.json()
        user      = self.get_or_create(user_info)
        token     = self.create_token(user.id)

        return JsonResponse({'token' : token}, status = 200)
        
    def get_or_create(self, user_info):
        user,flag = User.objects.get_or_create(
            kakao_id   = user_info['id'],
            is_host    = False,
            email      = user_info['kakao_account']['email'],
            nick_name  = user_info['properties']['nickname'],
            birth_date = user_info['kakao_account']['birthday'],
            is_adult   = int(user_info['kakao_account']['age_range'][0]) > 1
        )
        return user

    def create_token(self, user_id):
        token = jwt.encode({'user_id' : user_id , 'exp':datetime.utcnow() + timedelta(days = 3)}, settings.SECRET_KEY, settings.ALGORITHM)

        return token