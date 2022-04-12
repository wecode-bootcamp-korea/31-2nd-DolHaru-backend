from django.db import models

class User(models.Model):
    kakao_id    = models.IntegerField()
    is_host     = models.BooleanField(default=False)
    email       = models.CharField(max_length=300)
    first_name  = models.CharField(max_length=20)
    last_name   = models.CharField(max_length=20)
    birth_date  = models.DateField()
    created_at  = models.DateTimeField(auto_now_add = True)
    updatad_at  = models.DateTimeField(auto_now = True)
    
    class Meta:
        db_table = 'users'