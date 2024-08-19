from django.urls import path
from . import views

urlpatterns = [
    path('seller/dashboard/', views.seller_dashboard, name='seller_dashboard'),
    path('seller/manage-products/', views.manage_products, name='manage_products'),
    path('seller/add-product/', views.add_product, name='add_product'),
    path('seller/edit-product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('seller/delete-product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('seller/view-orders/', views.view_orders, name='view_orders'),
    path('seller/update-bank-details/', views.update_bank_details, name='update_bank_details'),
]
