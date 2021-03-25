from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_login, name = 'user_login'), 
    path('user-home/',views.user_home,name='user_home'),
    path('user-logout/', views.user_logout, name='user_logout'),
    path('user-signup/', views.user_signup, name = 'user_signup'),
    path('otp-generate/', views.otp_generate, name = 'otp_generate'),
    path('otp-validate/', views.otp_validate, name = 'otp_validate'),
    path('otp-resend/', views.otp_resend, name = 'otp_resend'),
    path('user-profile/', views.user_profile, name = 'user_profile'),
    path('set-propic/<int:id>', views.set_propic, name = 'set_propic'),
    path('sell-product/', views.sell_product, name = 'sell_product'),
    path('view-ad/<int:id>', views.view_ad, name = 'view_ad'),
    path('seller/<int:id>', views.view_seller, name = 'view_seller'),
]