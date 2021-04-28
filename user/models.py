from django.db import models
from django.contrib.auth.models import AbstractUser
from adminapp.models import *
from datetime import date, timedelta, datetime
# Create your models here.

class CustomUser(AbstractUser):
    profile_picture = models.ImageField(upload_to = 'pics', null = True)
    phone = models.BigIntegerField(null = True)
    district = models.CharField(max_length=50,null=True)

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
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    price = models.DecimalField(max_digits=20,decimal_places=2)
    fuel = models.CharField(max_length=50,null=True)
    date = models.DateField()
    expiry_date = models.DateField(null = True) 
    image1 = models.ImageField(null=True,upload_to='image')
    image2 = models.ImageField(null=True,upload_to='image')
    image3 = models.ImageField(null=True,upload_to='image')
    status = models.CharField(null=True,default='pending',max_length=10)
    location_latitude = models.CharField(max_length=20, null=True)
    location_longitude = models.CharField(max_length=20, null=True)
    brand_name = models.CharField(max_length=30, null=True)
    category_name = models.CharField(max_length=30, null=True)


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
            if self.expiry_date >= date.today():
                return True
            else:
                return False
        else:
            return False

class WishList(models.Model):
    ad = models.ForeignKey(UserAd, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    
class ReportAd(models.Model):
    ad = models.ForeignKey(UserAd, on_delete=models.CASCADE)
    note = models.TextField()
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    
class Follow(models.Model):
    follower = models.ForeignKey(CustomUser, on_delete = models.CASCADE,related_name='%(class)s_requests_follower')
    following = models.ForeignKey(CustomUser, on_delete = models.CASCADE,related_name='%(class)s_requests_following')
    
class PremiumMember(models.Model):
    premium_user = models.ForeignKey(CustomUser, on_delete = models.CASCADE)
    expiry_date = models.DateField() 
    
class FeturedAd(models.Model):
    ad = models.ForeignKey(UserAd, on_delete = models.CASCADE)
    expiry_date = models.DateField()
    
class OneToOne(models.Model):
    user1 = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='%(class)s_requests_created')
    user2 = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='%(class)s_requests_reciever') 
    ad = models.ForeignKey(UserAd, on_delete = models.CASCADE, null=True)
    room_name = models.CharField(max_length=100)
    
class Messages(models.Model):
    sender = models.ForeignKey(CustomUser(),on_delete=models.CASCADE,related_name='%(class)s_requests_sender')
    receiver = models.ForeignKey(CustomUser(),on_delete=models.CASCADE,related_name='%(class)s_requests_reciever')
    onetoone = models.ForeignKey(OneToOne,on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.now())
    message = models.TextField(null=True)
    msg_type = models.CharField(max_length=15,null=True)
    image = models.ImageField(upload_to='files',null=True)
    
    @property
    def get_image(self):
        try:
            return self.image.url
        except:
            return ''