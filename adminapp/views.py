from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.http import JsonResponse
from user.models import *
from .models import *
from django.contrib.auth.hashers import check_password
import requests
import json 
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
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
            data = response.text.encode('utf8')
            dict=json.loads(data.decode('utf8'))
            otp_id = dict["otp_id"]
            status = dict['status']
            if status == 'open':
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
        users = CustomUser.objects.filter().exclude(id = request.user.id).count()
        prime = PremiumMember.objects.all().count()
        ads = UserAd.objects.filter(expiry_date__gte = date.today()).count()
        
        fetured_ads = []
        fetured = FeturedAd.objects.filter(expiry_date__gte = date.today())

        for x in fetured:
            fetured_ads.append(x)
        
        prime_members = PremiumMember.objects.filter(expiry_date__gte = date.today())

        prime_members_list = []
        for x in prime_members:
            prime_members_list.append(x.premium_user.id)
        
        all_ads = UserAd.objects.filter(expiry_date__gte = date.today())
        for x in all_ads:
            if x.user.id in prime_members_list:
                if not x in fetured_ads:
                    fetured_ads.append(x)
                    
        # month chart     
        m1 = date.today() - timedelta(days = 30)
        m2 = m1 - timedelta(days = 30)
        m3 = m2 - timedelta(days = 30)
        m4 = m3 - timedelta(days = 30)
        m5 = m4 - timedelta(days = 30)
        m6 = m5 - timedelta(days = 30)
        m7 = m6 - timedelta(days = 30)
        m00 = date.today().strftime('%B')
        m01 = m1.strftime('%B')
        m02 = m2.strftime('%B')
        m03 = m3.strftime('%B')
        m04 = m4.strftime('%B')
        m05 = m5.strftime('%B')
        m06 = m6.strftime('%B')
        ads00 = UserAd.objects.filter(date__range = (m1,date.today())).count()
        ads01 = UserAd.objects.filter(date__range = (m2,m1)).count()
        ads02 = UserAd.objects.filter(date__range = (m3,m2)).count()
        ads03 = UserAd.objects.filter(date__range = (m4,m3)).count()
        ads04 = UserAd.objects.filter(date__range = (m5,m4)).count()
        ads05 = UserAd.objects.filter(date__range = (m6,m5)).count()
        ads06 = UserAd.objects.filter(date__range = (m7,m6)).count()
        
        # day chart
        d0 = date.today()
        d1 = d0 - timedelta(days=1)
        d2 = d1 - timedelta(days=1)
        d3 = d2 - timedelta(days=1)
        d4 = d3 - timedelta(days=1)
        d5 = d4 - timedelta(days=1)
        d6 = d5 - timedelta(days=1)
        day_ads0 = UserAd.objects.filter(date=d0).count()
        day_ads1 = UserAd.objects.filter(date=d1).count()
        day_ads2 = UserAd.objects.filter(date=d2).count()
        day_ads3 = UserAd.objects.filter(date=d3).count()
        day_ads4 = UserAd.objects.filter(date=d4).count()
        day_ads5 = UserAd.objects.filter(date=d5).count()
        day_ads6 = UserAd.objects.filter(date=d6).count()
        
        context = {
            'users':users,
            'ads':ads,
            'prime':prime,
            'fetured':len(fetured_ads),
            'm0':m00,
            'm1':m01,
            'm2':m02,
            'm3':m03,
            'm4':m04,
            'm5':m05,
            'm6':m06,
            'ads0':ads00,
            'ads1':ads01,
            'ads2':ads02,
            'ads3':ads03,
            'ads4':ads04,
            'ads5':ads05,
            'ads6':ads06,
            'd0':d0,
            'd1':d1,
            'd2':d2,
            'd3':d3,
            'd4':d4,
            'd5':d5,
            'd6':d6,
            'd_ad0':day_ads0,
            'd_ad1':day_ads1,
            'd_ad2':day_ads2,
            'd_ad3':day_ads3,
            'd_ad4':day_ads4,
            'd_ad5':day_ads5,
            'd_ad6':day_ads6,
            

        }
        return render(request,'admin/admin_home.html',context)
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
            attribute_list = request.POST.getlist('list[]')  
            km = False
            fuel = False
            if 'km_driven' in attribute_list:
                km = True
            if 'fuel' in attribute_list:
                fuel = True
            if Categories.objects.filter(category=category).exists():
                return JsonResponse('exist', safe=False)
            Categories.objects.create(category=category,km_driven=km,fuel=fuel)
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

def reports(request):
    if request.user.is_authenticated:
        from_date = date.today()-timedelta(days=30)
        ads = UserAd.objects.filter(date__range = (from_date,date.today()))
        status = 'true'
        if ads.count() == 0:
            status = 'false'
        print(status)
        context = {
            'ads':ads,'status': status
        }
        return render(request, 'admin/reports.html',context)
    else:
        return redirect(admin_login)
    
def report_from_to(request):
    if request.user.is_authenticated:
        from_date = request.GET['from_date']
        to_date = request.GET['to_date']
        ads = UserAd.objects.filter(date__range = (from_date,to_date))
        for x in ads:
            x.brand_name = x.brand.brand
            x.category_name = x.brand.category.category
        ser_ads = serializers.serialize('json',ads)
        context = {
            'ads':ser_ads,'status':'true'
        }
        return JsonResponse(context)
    else:
        return redirect(admin_login)
    
def report_key(request):
    if request.user.is_authenticated:
        key = request.GET['key']
        if key == 'Today':
            ads = UserAd.objects.filter(date=date.today())
        elif key == 'last_week':
            from_date = date.today()-timedelta(days=7)
            ads = UserAd.objects.filter(date__range = (from_date,date.today()))
        elif key == 'last_month':
            from_date = date.today()-timedelta(days=30)
            ads = UserAd.objects.filter(date__range = (from_date,date.today()))
        else:
            from_date = date.today() - timedelta(days=365)
            ads = UserAd.objects.filter(date__range = (from_date,date.today()))
        for x in ads:
            x.brand_name = x.brand.brand
            x.category_name = x.brand.category.category
        ser_ads = serializers.serialize('json',ads)
        context = {
            'ads':ser_ads,'status':'true'
        }
        return JsonResponse(context)
    else:
        return redirect(admin_login)