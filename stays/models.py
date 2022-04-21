from ctypes import addressof
from django.db      import models

class Stay(models.Model):
    user        = models.ForeignKey('users.User' , on_delete=models.CASCADE)
    title       = models.CharField(max_length=300)
    price       = models.DecimalField(max_digits=10, decimal_places=2)
    bed         = models.IntegerField(default=0)
    bedroom     = models.IntegerField(default=0)
    bathroom    = models.IntegerField(default=0)
    guest_adult = models.IntegerField(default=0)
    guest_kid   = models.IntegerField(default=0)
    guest_pet   = models.IntegerField(default=0)
    stay_type   = models.ForeignKey('StayType' , on_delete=models.CASCADE )
    description = models.CharField(max_length=400)
    address     = models.CharField(max_length=400)
    latitude    = models.DecimalField(max_digits=20, decimal_places=13)
    longitude   = models.DecimalField(max_digits=20, decimal_places=13)
    created_at  = models.DateTimeField(auto_now_add = True)
    updatad_at  = models.DateTimeField(auto_now = True)
    services    = models.ManyToManyField('Service', through = 'StayService')
    amenities   = models.ManyToManyField('Amenity', through = 'StayAmenity')
    highlight   = models.ManyToManyField('Highlight', through = 'StayHighlight')
    
    class Meta:
        db_table = 'stays'
    
    
class StayImage(models.Model):
    stay        = models.ForeignKey('Stay' , on_delete=models.CASCADE)
    image_url   = models.CharField(max_length=4000)
    
    class Meta:
        db_table ='stay_images'
        
class Service(models.Model):
    name = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'services'

class StayService(models.Model):
    service = models.ForeignKey('Service' , on_delete = models.CASCADE)
    stay    = models.ForeignKey('Stay' , on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'stay_services'
        
class StayHighlight(models.Model):
    stay        = models.ForeignKey('Stay' , on_delete=models.CASCADE)
    highlight   = models.ForeignKey('Highlight' , on_delete= models.CASCADE)
    
    class Meta:
        db_table = 'stay_highlights'
        
class Highlight(models.Model):
    name = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'highlights'
        
class Amenity(models.Model):
    name = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'amenities'

class StayAmenity(models.Model):
    stay      = models.ForeignKey('Stay' , on_delete = models.CASCADE)
    amenity   = models.ForeignKey('Amenity' , on_delete= models.CASCADE)

    class Meta:
        db_table = 'stay_amenities'
    
        
class StayType(models.Model):
    name      = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'stay_types'