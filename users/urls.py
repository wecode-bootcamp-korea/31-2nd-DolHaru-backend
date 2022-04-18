from django.urls import path

from users.views import *

urlpatterns = [
    path('/signin', KakaoSignInView.as_view())
]