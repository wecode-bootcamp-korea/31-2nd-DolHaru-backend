from django.db import models

class User(models.Model):
    kakao_id   = models.BigIntegerField()
    is_host    = models.BooleanField(default=False)
    is_adult   = models.BooleanField(default=False)
    email      = models.CharField(max_length=300)
    nick_name  = models.CharField(max_length=20)
    birth_date = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add = True)
    updatad_at = models.DateTimeField(auto_now = True)
    
    class Meta:
        db_table = 'users'