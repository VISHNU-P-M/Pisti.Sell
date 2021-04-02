from django.db import models
from django.contrib.auth.models import AbstractUser
from adminapp.models import *
from datetime import date, timedelta
# Create your models here.

class CustomUser(AbstractUser):
    profile_picture = models.ImageField(upload_to = 'pics', null = True)
    phone = models.BigIntegerField(null = True)

    @property
    def propic(self):
        try:
            return self.profile_picture.url
        except:
            return ''
    
class UserAd(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brands, on_delete=models.CASCADE)
    year = models.CharField(max_length=20)
    km_driven = models.DecimalField(decimal_places=2,max_digits=20)
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=500)
    price = models.DecimalField(max_digits=20,decimal_places=2)
    date = models.DateField()
    expiry_date = models.DateField(null = True) 
    image1 = models.ImageField(null=True,upload_to='image')
    image2 = models.ImageField(null=True,upload_to='image')
    image3 = models.ImageField(null=True,upload_to='image')
    status = models.CharField(null=True,default='pending',max_length=10)
    location_latitude = models.CharField(max_length=20, null=True)
    location_longitude = models.CharField(max_length=20, null=True)


    @property
    def img1(self):
        try:
            return self.image1.url
        except:
            return ''
    
    @property
    def img2(self):
        try:
            return self.image2.url
        except:
            return ''
        
    @property
    def img3(self):
        try:
            return self.image3.url
        except:
            return ''
    
    @property
    def active(self):
        if self.status == 'confirmed':
            if date.today()>(self.date + timedelta(days=14)):
                return False
            else:
                return True
        else:
            return False