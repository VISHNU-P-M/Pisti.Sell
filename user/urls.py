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
    path('view-images/<int:id>', views.view_images, name = 'view_images'),
    path('edit-ad/<int:id>', views.edit_ad, name = 'edit_ad'),
    path('seller/<int:id>', views.view_seller, name = 'view_seller'),
    path('add-wish-list/<int:id>', views.add_wishlist, name = 'add_wishlist'),
    path('view-wish-list/', views.view_wish_list, name = 'view_wish_list'),
    path('report-ad/',views.report_ad, name = 'report_ad'),
    path('location-filter/', views.location_filter, name = 'location_filter'),
    path('spec-filter/', views.spec_filter, name = 'spec_filter'),
    path('search-filter/', views.search_filter, name = 'search_filter'),
    path('follow-user/<int:id>', views.follow_user, name = 'follow_user'),
    path('get-premium/', views.get_premium, name = 'get_premium'),
    path('boost-ad/<int:id>', views.boost_ad, name = 'boost_ad'),
    path('chat/', views.chat, name = 'chat'),
    path('chat/<str:room_id>/', views.chat_room, name = 'chat_room')
]