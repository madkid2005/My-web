# accounts/urls.py
from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView


urlpatterns = [
    # SELLER 
    path('signup/seller/', views.seller_signup, name='seller_signup'),
    path('seller_dashboard/', views.seller_dashboard, name='seller_dashboard'),

    # BUYER
    path('signup/buyer/', views.buyer_signup, name='buyer_signup'),
    path('buyer/dashboard/', views.buyer_dashboard, name='buyer_dashboard'),
    path('profile/update/', views.update_buyer_profile, name='update_buyer_profile'),
    path('shipping/addresses/', views.manage_shipping_addresses, name='manage_shipping_addresses'),
    path('shipping/address/<int:id>/update/', views.update_shipping_address, name='update_shipping_address'),

    path('order/history/', views.order_history, name='order_history'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    
    #login
    path('login/', views.user_login, name='login'),

    # LOGOUT
    path('logout/', views.user_logout, name='logout'),
    # path('logout/', LogoutView.as_view, name='logout'),

]
