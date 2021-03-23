from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib.auth.models import User, auth
from .models import *
import requests
import json
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
        return render(request,'user/user_home.html')
    else:
        return redirect(user_login)

def user_logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        return redirect(user_login)
        