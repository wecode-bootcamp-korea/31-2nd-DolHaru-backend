from django.db import models

class Booking(models.Model):
    check_in    = models.DateTimeField()
    price       = models.DecimalField(max_digits=10, decimal_places=2)
    adult       = models.IntegerField(default=0)
    children    = models.IntegerField(default=0)
    pet         = models.IntegerField(default=0)
    status      = models.ForeignKey('Status', on_delete=models.CASCADE)
    user        = models.ForeignKey('users.User', on_delete=models.CASCADE)
    stay        = models.ForeignKey('staies.Stay', on_delete=models.CASCADE)
    
class Status(models.Model):
    name = models.CharField(max_length=200)