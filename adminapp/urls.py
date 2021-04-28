from django.urls import path
from . import views

urlpatterns = [
    path('' , views.admin_login, name = 'admin_login'),
    path('admin-home/', views.admin_home, name = "admin_home"), 
    path('admin-logout/', views.admin_logout, name="admin_logout"),
    path('otp-generate/', views.otp_generate, name='otp_generate'),
    path('otp-validate/', views.otp_validate, name='otp_validate'),
    path('otp-resend/', views.otp_resend, name = 'otp_resend'),
    path('users/', views.users, name = 'users'),
    path('block-user/<int:id>', views.block_user, name = 'block_user'),
    path('filter-user/', views.filter_user, name = 'filter_user'),
    path('categories/', views.view_categories, name = 'categories'),
    path('add-categories/', views.add_categories, name = 'add_categories'),
    path('delete-category/<int:id>', views.delete_category, name = 'delete_category'),
    path('brands/', views.view_brands, name = 'view_brands'),
    path('add-brands/', views.add_brands, name = 'add_brands'),
    path('delete-brand/<int:id>', views.delete_brand, name = 'delete_brand'),
    path('user-ads/', views.view_user_ads, name = 'view_user_ads'),
    path('fetured-ads/', views.view_fetured_ads, name = 'view_fetured_ads'),
    path('confirm-ad/<int:id>', views.confirm_ad, name = 'confirm_ad'),
    path('reject-ad/<int:id>', views.reject_ad, name = 'reject_ad'),
    path('user-reprots/', views.user_reports, name = 'user_reprots'),
    path('premium-users/', views.premium_users, name = 'premium_users'),
    path('reports/', views.reports, name = 'reports'),
    path('report-from-to/', views.report_from_to, name = 'report_from_to'),
    path('report-key/', views.report_key, name = 'report_key'),
]