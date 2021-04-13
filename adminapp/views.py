from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.http import JsonResponse
from user.models import *
from .models import *
from django.contrib.auth.hashers import check_password
import requests
import json 
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
def admin_login(request):
    if request.user.is_authenticated:
        return redirect(admin_home)
    else:
        if request.method=='POST':
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username,password=password)
            if user is not None:
                if user.is_superuser==True:
                    auth.login(request,user)
                    return JsonResponse('true',safe=False)
                else:
                    return JsonResponse('user',safe=False)
            else:
                return JsonResponse('false',safe=False)
        return render(request,'admin/login.html')

def otp_generate(request):
    if request.user.is_authenticated:
        return redirect(admin_home)
    else:
        if request.method == 'POST':
            phone = request.POST['phone']
            if CustomUser.objects.filter(phone=phone,is_superuser=True):
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
        else:
            return render(request,'admin/otp_generate.html')

def otp_validate(request):
    if request.user.is_authenticated:
        return redirect(admin_home)
    else:
        if request.method == 'POST':
            otp = request.POST['otp']
            #check
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
                user1 = CustomUser.objects.get(phone=phone)
                username = user1.username
                user = CustomUser.objects.filter(username=username).first()
                if user is not None:
                    auth.login(request,user,backend='django.contrib.auth.backends.ModelBackend' )
                    return JsonResponse('true',safe=False)
                else:
                    return JsonResponse('false', safe=False)
            else:
                return JsonResponse('false',safe=False)
        else:
            return redirect(admin_login)

def otp_resend(request):
    if request.user.is_authenticated:
        return redirect(admin_home)
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
            return redirect(admin_login)
        
def admin_logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        return redirect(admin_login)
    
def admin_home(request):
    if request.user.is_authenticated:
        return render(request,'admin/admin_home.html')
    else:
        return redirect(admin_login)    

def users(request):
    if request.user.is_authenticated:
        users = CustomUser.objects.filter(is_superuser=False)
        context = {'users':users}
        return render(request,'admin/users.html',context) 
    else:
        return redirect(admin_login)
    
def premium_users(request):
    if request.user.is_authenticated:
        premiumusers = PremiumMember.objects.filter(premium_user__is_superuser = False,expiry_date__gte = date.today())
        context = {
            'users':premiumusers
        }
        return render(request, 'admin/premium_users.html', context)
    else:
        return redirect(admin_login)

def block_user(request,id):
    if request.user.is_authenticated:
        user = CustomUser.objects.get(id=id)
        if user.is_active == True:
            user.is_active = False
        else:
            user.is_active = True
        user.save()
        return redirect(users)
    else:
        return redirect(admin_login)
    
def filter_user(request):
    if request.user.is_authenticated:
        key1 = request.GET['key']
        users = CustomUser.objects.filter(first_name__icontains=key1,is_superuser=False) or CustomUser.objects.filter(last_name__icontains = key1,is_superuser=False) or CustomUser.objects.filter(username__icontains=key1,is_superuser=False) or CustomUser.objects.filter(email__icontains=key1,is_superuser=False) or CustomUser.objects.filter(phone__icontains=key1,is_superuser=False)
        if users.count() != 0 :
            context = {'users':users,'key':key1}
        else:
            print('yes')
            context = {'exist':0,'key':key1}
        return render(request,'admin/users.html',context)
    else:
        return redirect(admin_login)

def view_categories(request):
    if request.user.is_authenticated:
        categories = Categories.objects.all()
        exist = True
        if categories.count() == 0 : 
            exist = False
        context = {'categories':categories,'exist':exist}
        return render(request,'admin/categories.html',context)
    else:
        return redirect(admin_login)

def add_categories(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            category = request.POST['category']
            if Categories.objects.filter(category=category).exists():
                return JsonResponse('exist', safe=False)
            Categories.objects.create(category=category)
            return JsonResponse('true', safe=False)
        else:
            return render(request, 'admin/add_categories.html')
    else:
        return redirect(admin_login)

def delete_category(request,id):
    if request.user.is_authenticated:
        category = Categories.objects.get(id=id)
        category.delete()
        return redirect(view_categories)
    else:
        return redirect(admin_login)
    
def view_brands(request):
    if request.user.is_authenticated:
        brands = Brands.objects.all()
        exist = True
        if brands.count() == 0:
            exist = False
        context = {'brands':brands,'exist':exist}
        return render(request, 'admin/brands.html', context)
    else:
        return redirect(admin_login)
    
def add_brands(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            category = request.POST['category']
            brand = request.POST['brand']
            if Brands.objects.filter(brand=brand,category=category):
                return JsonResponse('exist', safe=False)
            else:
                Brands.objects.create(category_id=category,brand=brand)
                return JsonResponse('true', safe=False)
        else:
            categories = Categories.objects.all()
            context = { 'categories':categories }
            return render(request, 'admin/add_brands.html' , context)
    else:
        return redirect(admin_login)
def delete_brand(request,id):
    if request.user.is_authenticated:
        brand = Brands.objects.get(id=id)
        brand.delete()
        return redirect(view_brands)
    else:
        return redirect(admin_login)
    
def view_user_ads(request):
    if request.user.is_authenticated:
        user_ads = UserAd.objects.all()
        exist = True
        if user_ads.count() == 0:
            exist = False
        context = {
            'user_ads':user_ads,
            'exist':exist
        }
        return render(request, 'admin/view_user_ads.html',context)
    else:
        return redirect(admin_login)
    
def view_fetured_ads(request):
    if request.user.is_authenticated:
        fetured_ads_list = []
        fetured_ads = FeturedAd.objects.filter(expiry_date__gte = date.today())
        for x in fetured_ads:
            fetured_ads_list.append(x.ad)
        premiumusers = []
        premiums = PremiumMember.objects.all()
        for x in premiums:
            premiumusers.append(x.premium_user_id)
        for x in premiumusers:
            premium_ads = UserAd.objects.filter(user_id = x)
            for y in premium_ads:
                fetured_ads_list.append(y)
            
        exist = True
        if len(fetured_ads_list) == 0:
            exist = False
        context = {
            'user_ads':fetured_ads_list,
            'exist':exist
        }
        return render(request, 'admin/view_fetured_ads.html',context)
    else:
        return redirect(admin_login)    


def confirm_ad(request,id):
    if request.user.is_authenticated:
        ad = UserAd.objects.get(id=id)
        ad.status = 'confirmed'
        ad.save()
        return redirect(view_user_ads)
    else:
        return redirect(admin_login)
@csrf_exempt  
def reject_ad(request,id):
    if request.user.is_authenticated:
        ad = UserAd.objects.get(id=id)
        if ad.status == 'confirmed':
            ad.status = 'rejected'
        else:
            ad.status = 'confirmed'
        ad.save()
        return JsonResponse('true',safe=False)
    else:
        return redirect(admin_login)
    
def user_reports(request):
    if request.user.is_authenticated:
        reports = ReportAd.objects.all()
        if reports.count() == 0:
            exist = 0
        else:
            exist = 1
        context = {
            'reports':reports,
            'exist': exist
        }  
        return render(request, 'admin/user_reprots.html', context)
    else:
        return redirect(admin_login)