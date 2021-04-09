from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib.auth.models import User, auth
from .models import *
from adminapp.models import *
import requests
import json
from django.views.decorators.csrf import csrf_exempt
from django.core.files import File
from datetime import date, timedelta
import folium

# watermark on image
import cv2
import numpy as np
from PIL import Image

# import StringIO

# from django.core.files.uploadedfile import InMemoryUploadedFile

# geolocation
from geopy.geocoders import Nominatim
from django.contrib.gis.geoip2 import GeoIP2 
from geopy.distance import geodesic

# map stuff fron end
import pandas as pd
from folium.plugins import MarkerCluster
from folium.plugins import Search


#for convert base64 to imagefile
import base64
from django.core.files.base import ContentFile


# Create your views here.
def user_login(request):
    if request.user.is_authenticated:
        return redirect(user_home)
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request,user)
                return JsonResponse('true', safe=False)
            else:
                return JsonResponse('false', safe=False)
        else:
            return render(request,'user/login.html')

def user_signup(request):
    if request.user.is_authenticated:
        return redirect(user_home)
    else:
        if request.method == 'POST':
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            username = request.POST['username']
            email = request.POST['email']
            phone = request.POST['phone']
            district = request.POST['district']
            password = request.POST['password']
            if CustomUser.objects.filter(username=username).exists():
                return JsonResponse('user', safe=False)
            elif CustomUser.objects.filter(email=email).exists():
                return JsonResponse('email', safe=False)
            elif CustomUser.objects.filter(phone=phone).exists():
                return JsonResponse('phone', safe=False)
            else:
                CustomUser.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,phone=phone,district=district,password=password)
                return JsonResponse('true', safe=False)
        else:
            return redirect(user_login)

def otp_generate(request):
    if request.user.is_authenticated:
        return redirect(user_home)
    else:
        if request.method == 'POST':
            phone = request.POST['phone']
            if CustomUser.objects.filter(phone=phone).exists():
                url = "https://d7networks.com/api/verifier/send"
                phone1 = '91'+str(phone)
                payload = {'mobile': phone1,
                'sender_id': 'SMSINFO',
                'message': 'Your otp code is {code}',
                'expiry': '900'} 
                files = [

                ]
                headers = {
                'Authorization': 'Token cbad324544bd072bb68feb55055c0f79085f1bd7'
                }

                response = requests.request("POST", url, headers=headers, data = payload, files = files)
                print(response.text)
                data = response.text.encode('utf8')
                dict=json.loads(data.decode('utf8'))
                otp_id = dict["otp_id"]
                print(otp_id)
                request.session['otp_id'] = otp_id
                request.session['phone'] = phone
                status = dict['status']
                if status == 'open':
                    request.session['otp_id'] = otp_id
                    return JsonResponse('true', safe=False)
                else:
                    return JsonResponse('false', safe=False)
            else:
                return JsonResponse('false',safe=False)
        return render(request,'user/otp_generate.html')
    
def otp_validate(request):
    if request.user.is_authenticated:
        return redirect(user_home)
    else:
        if request.method == 'POST':
            otp = request.POST['otp']
            phone = request.session['phone']
            url = "https://d7networks.com/api/verifier/verify"
            otp_id = request.session['otp_id']
            del request.session['otp_id']
            payload = {'otp_id': otp_id ,
            'otp_code': otp}
            files = [

            ]
            headers = {
            'Authorization': 'Token cbad324544bd072bb68feb55055c0f79085f1bd7'
            }

            response = requests.request("POST", url, headers=headers, data = payload, files = files)
            print(response.text)
            data = response.text.encode('utf8')
            dict=json.loads(data.decode('utf8'))
            status = dict['status']
            if status == 'success':
                user = CustomUser.objects.get(phone=phone)
                auth.login(request,user)
                return JsonResponse('true',safe=False)
            else:
                return JsonResponse('false',safe=False)
        return redirect(user_login)

def otp_resend(request):
    if request.user.is_authenticated:
        return redirect(user_home)
    else:
        if request.method == 'POST':
            otp_id = request.session['otp_id']
            url = "https://d7networks.com/api/verifier/resend"
            payload={'otp_id': otp_id}
            files=[

            ]
            headers = {
            'Authorization': 'Token cbad324544bd072bb68feb55055c0f79085f1bd7'
            }

            response = requests.request("POST", url, headers=headers, data=payload, files=files)
            print(response.text)
            data = response.text.encode('utf8')
            dict=json.loads(data.decode('utf8'))
            otp_id = dict["otp_id"]
            status = dict['status']
            if status == 'open':
                print(otp_id)
                print('resend')
                return JsonResponse('true', safe=False)
            else:
                return JsonResponse('false',safe=False)
        else:
            return redirect(user_login)

def user_home(request):
    if request.user.is_authenticated:
        ads = UserAd.objects.filter(status='confirmed',expiry_date__gt=date.today()).exclude(user=request.user)
        district = request.user.district
        geolocator = Nominatim(user_agent="user")
        location = geolocator.geocode(district)
        latitude,longitude = location.latitude, location.longitude
        
        user_location = (latitude,longitude)
        
        all_ads_id = []
        all_ads = UserAd.objects.filter(status='confirmed').exclude(user=request.user)
        
        
        # for finding the ad near user location
        for ad in all_ads:
            ad_location = (ad.location_latitude,ad.location_longitude)
            print(request.user.district)
            print(geodesic(user_location,ad_location).km)
            if geodesic(user_location,ad_location).km <100:
                all_ads_id.append(ad.id)
                
                
        wish_list = []
        Wishes = WishList.objects.filter(user=request.user)
        for wish in Wishes:
            wish_list.append(wish.ad.id)
        context = {
            'ads':ads,
            'all_ads':all_ads,
            'ads_id':all_ads_id,
            'wish_list':wish_list,
        }
        return render(request,'user/user_home.html', context)
    else:
        return redirect(user_login)

def user_logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        return redirect(user_login)

def user_profile(request):
    if request.user.is_authenticated:
        user = request.user
        followers = Follow.objects.filter(following = user)
        count_followers = followers.count()
        print(count_followers)
        followings = Follow.objects.filter(follower = user)
        count_followings = followings.count()
        print(count_followings) 
        if UserAd.objects.filter(user=user).exists():
            userad = UserAd.objects.filter(user=user)
            context = {
            'user':user,
            'userad':userad,
            'followers':followers,
            'count_followers':count_followers,
            'followings':followings,
            'count_followings':count_followings
            }
        else:
            context = {
            'user':user,
            'followers':followers,
            'count_followers':count_followers,
            'followings':followings,
            'count_followings':count_followings
            }
        return render(request, 'user/user_profile.html', context)
    else:
        return redirect(user_login)
    
@csrf_exempt   
def set_propic(request,id):
    if request.user.is_authenticated:
        propic = request.FILES.get('profilepic')
        user = CustomUser.objects.get(id=id)
        user.profile_picture=propic
        user.save()
        print(propic)
        return JsonResponse('true',safe=False)
    else:
        return redirect(user_login)

def get_geo(ip):
    g = GeoIP2()
    country = g.country(ip)
    city = g.city(ip)
    lat, lon = g.lat_lon(ip)
    return country, city, lat, lon

def get_ip_address(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@csrf_exempt
def sell_product(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            # ----------------WITHOUT CROPING-----------------
            # img1 = request.FILES.get('img1')
            # img2 = request.FILES.get('img2')
            # img3 = request.FILES.get('img3')
            
            # brand = request.POST.get('brand')
            # year = request.POST.get('year')
            # km = request.POST.get('km')
            # title = request.POST.get('title')
            # description = request.POST.get('description')
            # price = request.POST.get('price')
            # latitude = request.session['latitude']
            # longitude = request.session['longitude']
            # del request.session['latitude']
            # del request.session['longitude']
            # today = date.today()
            # expiry = today + timedelta(days=14)
            # if UserAd.objects.filter(user=request.user,expiry_date__gt=today).count()>=2:
            #     return JsonResponse('false', safe=False)
            # else:
            #     user_ad = UserAd.objects.create(user=request.user,brand_id=brand,year=year,km_driven=km,title=title,description=description,
            #                                     price=price,date=today,expiry_date=expiry,image1=img1,image2=img2,image3=img3,
            #                                     location_latitude=latitude,location_longitude=longitude)
            #     # importing logo
            #     logo = cv2.imread('static/images/Logo.png')
            #     logo_height, logo_width, _ = logo.shape
                    
            #     #set first image logo
            #     image1 = cv2.imread('static/'+user_ad.img1)
            #     image1_height, image1_width, _ = image1.shape
            #     # print('height and width',image_height,image_width)
            #     top1_y = image1_height - logo_height
            #     left1_x = image1_width - logo_width
            #     # print(top_y,left_x)
            #     roi1 = image1[top1_y:image1_height,left1_x:image1_width] 
            #     result1 = cv2.addWeighted(roi1, 1, logo, 0.5, 0)
            #     image1[top1_y:image1_height,left1_x:image1_width] = result1
            #     # cv2.imshow('image1', image1)
            #     # cv2.waitKey(0)
            #     print('logoset')
            #     cv2.imwrite('static/'+user_ad.img1,image1)
                
            #     #set second image logo
            #     image2 = cv2.imread('static/'+user_ad.img2)
            #     image2_height, image2_width, _ = image2.shape
            #     # print('height and width',image_height,image_width)
            #     top2_y = image2_height - logo_height
            #     left2_x = image2_width - logo_width
            #     # print(top_y,left_x)
            #     roi2 = image2[top2_y:image2_height,left2_x:image2_width] 
            #     result2 = cv2.addWeighted(roi2, 1, logo, 0.5, 0)
            #     image2[top2_y:image2_height,left2_x:image2_width] = result2
            #     # cv2.imshow('image1', image1)
            #     # cv2.waitKey(0)
            #     print('logoset')
            #     cv2.imwrite('static/'+user_ad.img2,image2)
                
            #     #set third image logo
            #     image3 = cv2.imread('static/'+user_ad.img3)
            #     image3_height, image3_width, _ = image3.shape
            #     # print('height and width',image_height,image_width)
            #     top3_y = image3_height - logo_height
            #     left3_x = image3_width - logo_width
            #     # print(top_y,left_x)
            #     roi3 = image3[top3_y:image3_height,left3_x:image3_width] 
            #     result3 = cv2.addWeighted(roi3, 1, logo, 0.5, 0)
            #     image3[top3_y:image3_height,left3_x:image3_width] = result3
            #     # cv2.imshow('image1', image1)
            #     # cv2.waitKey(0)
            #     print('logoset')
            #     cv2.imwrite('static/'+user_ad.img3,image3)
                
            #     return JsonResponse('true', safe=False)
            
            # ---------WITH CROPING----------
            title = request.POST['title']
            img1 = request.POST['img1']
            # converting to file
            format, imgstr = img1.split(';base64,')
            ext1 = format.split('/')[-1]
            imageurl1 = ContentFile(base64.b64decode(imgstr), name=title + '1.' + ext1)
            
            img2 = request.POST['img2']
            # converting to file
            format, imgstr = img2.split(';base64,')
            ext2 = format.split('/')[-1]
            imageurl2 = ContentFile(base64.b64decode(imgstr), name=title + '2.' + ext2)
            
            img3 = request.POST['img3']
            # converting to file
            format, imgstr = img3.split(';base64,')
            ext3 = format.split('/')[-1]
            imageurl3 = ContentFile(base64.b64decode(imgstr), name=title + '3.' + ext3)
            
            brand = request.POST['brand']
            year = request.POST['year']
            km = request.POST['km']
            description = request.POST['description']
            price = request.POST['price']
            district = request.POST['district']
            if district == '0':
                latitude = request.session['latitude']
                longitude = request.session['longitude']
            else:
                geolocator = Nominatim(user_agent="user")
                location = geolocator.geocode(district)
                latitude,longitude = location.latitude, location.longitude
            del request.session['latitude']
            del request.session['longitude']
            today = date.today()
            expiry = today + timedelta(days=14)
            if UserAd.objects.filter(user=request.user,expiry_date__gt=today).count()>=2:
                return JsonResponse('false', safe=False)
            else:
                user_ad = UserAd.objects.create(user=request.user,brand_id=brand,year=year,km_driven=km,title=title,description=description,
                                                price=price,date=today,expiry_date=expiry,image1=imageurl1,image2=imageurl2,image3=imageurl3,
                                                location_latitude=latitude,location_longitude=longitude)
                # importing logo
                logo = cv2.imread('static/images/Logo.png')
                logo_height, logo_width, _ = logo.shape
                    
                #set first image logo
                image1 = cv2.imread('static/'+user_ad.img1)
                image1_height, image1_width, _ = image1.shape
                # print('height and width',image_height,image_width)
                top1_y = image1_height - logo_height
                left1_x = image1_width - logo_width
                # print(top_y,left_x)
                roi1 = image1[top1_y:image1_height,left1_x:image1_width] 
                result1 = cv2.addWeighted(roi1, 1, logo, 0.5, 0)
                image1[top1_y:image1_height,left1_x:image1_width] = result1
                # cv2.imshow('image1', image1)
                # cv2.waitKey(0)
                cv2.imwrite('static/'+user_ad.img1,image1)
                
                #set second image logo
                image2 = cv2.imread('static/'+user_ad.img2)
                image2_height, image2_width, _ = image2.shape
                # print('height and width',image_height,image_width)
                top2_y = image2_height - logo_height
                left2_x = image2_width - logo_width
                # print(top_y,left_x)
                roi2 = image2[top2_y:image2_height,left2_x:image2_width] 
                result2 = cv2.addWeighted(roi2, 1, logo, 0.5, 0)
                image2[top2_y:image2_height,left2_x:image2_width] = result2
                # cv2.imshow('image1', image1)
                # cv2.waitKey(0)
                cv2.imwrite('static/'+user_ad.img2,image2)
                
                #set third image logo
                image3 = cv2.imread('static/'+user_ad.img3)
                image3_height, image3_width, _ = image3.shape
                # print('height and width',image_height,image_width)
                top3_y = image3_height - logo_height
                left3_x = image3_width - logo_width
                # print(top_y,left_x)
                roi3 = image3[top3_y:image3_height,left3_x:image3_width] 
                result3 = cv2.addWeighted(roi3, 1, logo, 0.5, 0)
                image3[top3_y:image3_height,left3_x:image3_width] = result3
                # cv2.imshow('image1', image1)
                # cv2.waitKey(0)
                cv2.imwrite('static/'+user_ad.img3,image3)
                
                return JsonResponse('true', safe=False)
        else:
            geolocator = Nominatim(user_agent="user")
            o_ip = get_ip_address(request)
            # print(o_ip)
            ip = '117.194.167.44'
            country, city , lat, lon = get_geo(ip)
            request.session['latitude'] = lat
            request.session['longitude'] = lon
            location = geolocator.geocode(city)
            point = ([lat,lon])
            
            # folium map
            folium_map_ = folium.Map(width=400, height=250, location=point, zoom_start = 15) 
            folium.Marker([lat,lon], icon = folium.Icon(color = 'red')).add_to(folium_map_)
            
            
            folium_map = folium_map_._repr_html_()
            
            categories = Categories.objects.all()
            brands = Brands.objects.all()
            context = {
                'categories':categories,
                'brands':brands,
                'map':folium_map
            }
            return render(request, 'user/sell_product.html',context)    
            
    else:
        return redirect(user_login)
    
    
@csrf_exempt

def edit_ad(request, id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            brand = request.POST.get('brand')
            year = request.POST.get('year')
            km = request.POST.get('km')
            title = request.POST.get('title')
            description = request.POST.get('description')
            price = request.POST.get('price')
            latitude = request.session['latitude']
            longitude = request.session['longitude']
            del request.session['latitude']
            del request.session['longitude']
            
            ad = UserAd.objects.get(id=id)
            
            if 'img1' not in request.POST:
                img1 = request.FILES.get('img1')
            else:
                img1 = ad.image1
            if 'img2' not in request.POST:
                img2 = request.FILES.get('img2')
            else:
                img2 = ad.image2
            if 'img3' not in request.POST:
                img3 = request.FILES.get('img3')
            else:
                img3 = ad.image3
                
            print(brand,year,km,title,description,price,latitude,longitude,img1,img2,img3)
            ad.brand_id = brand
            ad.year = year
            ad.km_driven = km
            ad.title = title
            ad.description = description
            ad.price = price
            ad.location_latitude = latitude
            ad.location_longitude = longitude
            ad.image1 = img1
            ad.image2 = img2
            ad.image3 = img3
            ad.save()
            # importing logo
            logo = cv2.imread('static/images/Logo.png')
            logo_height, logo_width, _ = logo.shape
            
            if 'img1' not in request.POST:
                #set first image logo
                image1 = cv2.imread('static/'+ad.img1)
                image1_height, image1_width, _ = image1.shape
                top1_y = image1_height - logo_height
                left1_x = image1_width - logo_width
                roi1 = image1[top1_y:image1_height,left1_x:image1_width] 
                result1 = cv2.addWeighted(roi1, 1, logo, 0.5, 0)
                image1[top1_y:image1_height,left1_x:image1_width] = result1
                cv2.imwrite('static/'+ad.img1,image1)
                
            if 'img2' not in request.POST:
                image2 = cv2.imread('static/'+ad.img2)
                image2_height, image2_width, _ = image2.shape
                top2_y = image2_height - logo_height
                left2_x = image2_width - logo_width
                roi2 = image2[top2_y:image2_height,left2_x:image2_width] 
                result2 = cv2.addWeighted(roi2, 1, logo, 0.5, 0)
                image2[top2_y:image2_height,left2_x:image2_width] = result2
                cv2.imwrite('static/'+ad.img2,image2)
                
            if 'img3' not in request.POST:  
                image3 = cv2.imread('static/'+ad.img3)
                image3_height, image3_width, _ = image3.shape
                top3_y = image3_height - logo_height
                left3_x = image3_width - logo_width
                roi3 = image3[top3_y:image3_height,left3_x:image3_width] 
                result3 = cv2.addWeighted(roi3, 1, logo, 0.5, 0)
                image3[top3_y:image3_height,left3_x:image3_width] = result3
                cv2.imwrite('static/'+ad.img3,image3)
                
            return JsonResponse('true', safe=False)
        else:
            ad = UserAd.objects.get(id=id)
            categories = Categories.objects.all()
            brands = Brands.objects.all()
            
            request.session['latitude'] = ad.location_latitude
            request.session['longitude'] = ad.location_longitude
            point = ([ad.location_latitude,ad.location_longitude])
            
            # folium map
            folium_map_ = folium.Map(width=400, height=250, location=point, zoom_start = 15) 
            folium.Marker([ad.location_latitude,ad.location_longitude], icon = folium.Icon(color = 'red')).add_to(folium_map_)
            
            
            folium_map = folium_map_._repr_html_()
            
            context = {
                'ad': ad, 
                'map':folium_map,
                'categories':categories,
                'brands':brands,
            }
            return render(request, 'user/edit_ad.html',context)
    else:
        return redirect(user_login)


def view_ad(request,id):
    if request.user.is_authenticated:
        ad = UserAd.objects.get(id=id)
        point = ([ad.location_latitude,ad.location_longitude])
        folium_map_ = folium.Map(width=300, height=200, location=point, zoom_start = 15) 
        folium.Marker([ad.location_latitude,ad.location_longitude], icon = folium.Icon(color = 'red')).add_to(folium_map_)
        folium_map = folium_map_._repr_html_()
        wish_list =[]
        wishlist = WishList.objects.filter(user=request.user)
        for wish in wishlist:
            wish_list.append(wish.ad.id)
        if ad.user == request.user:
            context = {
                'own': True,
                'ad' : ad,
                'wish_list':wish_list,
                'map':folium_map
            }
        else:
            context = {
                'own': False,
                'ad':ad,
                'wish_list':wish_list,
                'map':folium_map
            }
        return render(request,'user/view_ad.html',context)
    else:
        return redirect(user_login)
    
def view_seller(request,id):
    if request.user.is_authenticated:
        seller = CustomUser.objects.get(id=id)
        
        # check is following or not
        if Follow.objects.filter(follower=request.user,following=seller).exists():
            is_following = True
        else:
            is_following = False
        # getting the followers and followings
        followers = Follow.objects.filter(following = seller)
        count_followers = followers.count()
        print(count_followers)
        followings = Follow.objects.filter(follower=seller)
        count_followings = followings.count()
        print(count_followings) 
        if UserAd.objects.filter(user=seller).exists():
            ads = UserAd.objects.filter(user=seller)
            wish_list =[]
            wishlist = WishList.objects.filter(user=request.user)
            for wish in wishlist:
                wish_list.append(wish.ad.id)
            context = {
                'seller':seller,
                'ads':ads,
                'wish_list':wish_list,
                'is_following':is_following,
                'followers':followers,
                'count_followers':count_followers,
                'followings':followings,
                'count_followings':count_followings
            }
        else:
            context = {
                'seller':seller,
                'is_following':is_following,
                'followers':followers,
                'count_followers':count_followers,
                'followings':followings,
                'count_followings':count_followings
            }
        return render(request,'user/seller_profile.html', context)
    else:
        return redirect(user_login)
    
def follow_user(request,id):
    if request.user.is_authenticated:
        follower = request.user
        following_id = id
        if Follow.objects.filter(follower = follower,following_id = following_id).exists():
            follow = Follow.objects.filter(follower = follower , following_id = following_id)
            follow.delete()
            return JsonResponse('follow', safe=False)
        else:
            Follow.objects.create(follower = follower,following_id = following_id)
            print('followed')
            return JsonResponse('unfollow',safe=False)
    else:
        return redirect(user_login)
    
def add_wishlist(request,id):
    ad = UserAd.objects.get(id=id)
    if WishList.objects.filter(ad=ad,user=request.user).exists():
        wish = WishList.objects.filter(ad=ad,user=request.user).first()
        wish.delete()
        return JsonResponse('removed',safe=False)
    else:
        WishList.objects.create(ad=ad,user=request.user)
        return JsonResponse('added',safe=False)
    return JsonResponse('false',safe=False)

def view_wish_list(request):
    if request.user.is_authenticated:
        wish_list = WishList.objects.filter(user=request.user)
        wish_lists = []
        Wishes = WishList.objects.filter(user=request.user)
        for wish in Wishes:
            wish_lists.append(wish.ad.id)
        context = {
            'wish_list':wish_list,
            'wish_lists':wish_lists
        }
        return render(request, 'user/view_wish_list.html',context)
    else:
        return redirect(user_login)

def report_ad(request):
    if request.user.is_authenticated:
        ad_id = request.GET["ad_id"]
        note = request.GET['note']
        if ReportAd.objects.filter(ad_id = ad_id,user=request.user).exists():
            return JsonResponse('false',safe = False)
        else:
            ReportAd.objects.create(ad_id = ad_id,note = note, user = request.user)
            return JsonResponse('true',safe = False)
    else:
        return redirect(user_login)
    
def view_images(request,id):
    if request.user.is_authenticated:
        ad = UserAd.objects.get(id=id)
        context = {
            'ad':ad,
            'id':id 
        }
        return render(request, 'user/view_images.html', context)
    else:
        return redirect(user_login)
    
def location_filter(request):
    if request.user.is_authenticated:
        district = request.GET['district']
        print(district)
        geolocator = Nominatim(user_agent="user")
        location = geolocator.geocode(district)
        latitude,longitude = location.latitude, location.longitude
        filter_location = (latitude,longitude)
        filtered_ads = []
        all_ads = UserAd.objects.filter(status='confirmed').exclude(user=request.user)
        # for finding the ad near user location
        for ad in all_ads:
            ad_location = (ad.location_latitude,ad.location_longitude)
            print(geodesic(filter_location,ad_location).km)
            if geodesic(filter_location,ad_location).km <100:
                filtered_ads.append(ad)
        # for geting ads in wishlist
        wish_list = []
        Wishes = WishList.objects.filter(user=request.user)
        for wish in Wishes:
            wish_list.append(wish.ad.id)
        categories = Categories.objects.all()
        brands = Brands.objects.all()
        context = {
            'district':district,
            'ads':filtered_ads,
            'wish_list':wish_list,
            'categories':categories,
            'brands':brands 
        }
        return render(request, 'user/filter.html', context )
    else:
        return redirect(user_login)
    
def search_filter(request):
    if request.user.is_authenticated:
        key = request.GET['key']
        ads1 = UserAd.objects.filter(brand__brand__icontains = key).exclude(user=request.user)
        ads2 = UserAd.objects.filter(brand__category__category__icontains = key).exclude(user=request.user)
        ads3 = UserAd.objects.filter(title__icontains = key).exclude(user=request.user)
        exist = True
        ads = []
        for ad in ads1:
            ads.append(ad)
        for ad in ads2:
            if ad in ads:
                pass
            else:
                ads.append(ad)
        for ad in ads3:
            if ad in ads:
                pass
            else:
                ads.append(ad)
        
        wish_list = []
        wishlist = WishList.objects.filter(user=request.user)
        for wish in wishlist:
            wish_list.append(wish.ad.id)
            
        categories = Categories.objects.all()
        brands = Brands.objects.all()
        
        district = request.user.district
        geolocator = Nominatim(user_agent="user")
        location = geolocator.geocode(district)
        latitude,longitude = location.latitude, location.longitude
        
        user_location = (latitude,longitude)
        filter_ads = []
        # for finding the ad near user location
        for ad in ads:
            ad_location = (ad.location_latitude,ad.location_longitude)
            print(geodesic(user_location,ad_location).km)
            if geodesic(user_location,ad_location).km <100:
                filter_ads.append(ad)
        if len(filter_ads) == 0:
            exist = False 
        print(len(filter_ads))     
        context = {
            'ads':filter_ads,
            'district':district,
            'exist':exist,
            'wish_list':wish_list,
            'categories':categories,
            'brands':brands
        }
        return render(request, 'user/filter.html', context)
    else:
        return redirect(user_login)
    
def spec_filter(request):
    if request.user.is_authenticated:
        district = request.GET['district_']
        category_id = request.GET['category']
        brand_id = request.GET['brand']
        from_price = request.GET['from_price']
        to_price = request.GET['to_price']
        if category_id == '0':
            print('only price')
            ads = UserAd.objects.filter(price__range=(float(from_price),float(to_price))).exclude(user=request.user)
        elif brand_id == '0' and from_price == '':
            print('only category')
            ads = UserAd.objects.filter(brand__category_id = category_id) .exclude(user=request.user)
        elif brand_id == '0' and from_price != '':
            print('no brand and have price')
            ads = UserAd.objects.filter(brand__category_id=category_id,price__range=(float(from_price),float(to_price))).exclude(user=request.user)
        elif from_price == '' and brand_id != '0':
            print('no price and have brand')
            ads = UserAd.objects.filter(brand_id = brand_id,brand__category_id=category_id).exclude(user=request.user)
        else:
            print('all have')
            ads = UserAd.objects.filter(brand__category_id=category_id,brand_id = brand_id,price__range=(float(from_price),float(to_price))).exclude(user=request.user) 
        
        geolocator = Nominatim(user_agent="user")
        location = geolocator.geocode(district)
        latitude,longitude = location.latitude, location.longitude
        filter_location = (latitude,longitude)
        filtered_ads = []
        
        # for finding the ad near user location
        for ad in ads:
            ad_location = (ad.location_latitude,ad.location_longitude)
            print(geodesic(filter_location,ad_location).km)
            if geodesic(filter_location,ad_location).km <100:
                filtered_ads.append(ad)
                
        # for getting ads in wishlist
        wish_list = []
        Wishes = WishList.objects.filter(user=request.user)
        for wish in Wishes:
            wish_list.append(wish.ad.id)
        
        if len(filtered_ads)== 0:
            exist = False
        else:
            exist = True
        
        categories = Categories.objects.all()
        brands = Brands.objects.all()
        context = {
            'ads':filtered_ads,
            'exist':exist,
            'wish_list':wish_list,
            'district':district,
            'categories':categories,
            'brands':brands,
        }
        return render(request, 'user/filter.html', context)
    else:
        return redirect(user_login)
    
