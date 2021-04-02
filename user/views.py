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

#geolocation
from geopy.geocoders import Nominatim
from django.contrib.gis.geoip2 import GeoIP2 

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
            password = request.POST['password']
            print(first_name,last_name,username,email,phone,password)
            if CustomUser.objects.filter(username=username).exists():
                return JsonResponse('user', safe=False)
            elif CustomUser.objects.filter(email=email).exists():
                return JsonResponse('email', safe=False)
            elif CustomUser.objects.filter(phone=phone).exists():
                return JsonResponse('phone', safe=False)
            else:
                CustomUser.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,phone=phone,password=password)
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
        all_ads = UserAd.objects.filter(status='confirmed')
        context = {
            'ads':ads,
            'all_ads':all_ads
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
        if UserAd.objects.filter(user=user).exists():
            userad = UserAd.objects.filter(user=user)
            context = {
            'user':user,
            'userad':userad
            }
        else:
            context = {
            'user':user,
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
            img1 = request.FILES.get('img1')
            img2 = request.FILES.get('img2')
            img3 = request.FILES.get('img3')
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
            today = date.today()
            expiry = today + timedelta(days=14)
            print(latitude,longitude)
            if UserAd.objects.filter(user=request.user,expiry_date__gt=today).count()>2:
                return JsonResponse('false', safe=False)
            else:
                UserAd.objects.create(user=request.user,brand_id=brand,year=year,km_driven=km,title=title,description=description,
                                      price=price,date=today,expiry_date=expiry,image1=img1,image2=img2,image3=img3,
                                      location_latitude=latitude,location_longitude=longitude)
                return JsonResponse('true',safe=False)
        else:
            geolocator = Nominatim(user_agent="user")
            o_ip = get_ip_address(request)
            print(o_ip)
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

def view_ad(request,id):
    if request.user.is_authenticated:
        ad = UserAd.objects.get(id=id)
        point = ([ad.location_latitude,ad.location_longitude])
        folium_map_ = folium.Map(width=300, height=200, location=point, zoom_start = 15) 
        folium.Marker([ad.location_latitude,ad.location_longitude], icon = folium.Icon(color = 'red')).add_to(folium_map_)
        folium_map = folium_map_._repr_html_()
        if ad.user == request.user:
            context = {
                'own': True,
                'ad' : ad,
                'map':folium_map
            }
        else:
            context = {
                'own': False,
                'ad':ad,
                'map':folium_map
            }
        return render(request,'user/view_ad.html',context)
    else:
        return redirect(user_login)
    
def view_seller(request,id):
    if request.user.is_authenticated:
        seller = CustomUser.objects.get(id=id)
        if UserAd.objects.filter(user=seller).exists():
            ads = UserAd.objects.filter(user=seller)
            context = {
                'seller':seller,
                'ads':ads
            }
        else:
            context = {
                'seller':seller
            }
        return render(request,'user/seller_profile.html', context)
    else:
        return redirect(user_login)