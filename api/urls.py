from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from . import views

urlpatterns = [
    # Authentication - exempt from CSRF
    path('auth/register/', csrf_exempt(views.register), name='register'),
    path('auth/login/', csrf_exempt(views.login), name='login'),
    path('auth/profile/', views.get_user_profile, name='profile'),
    
    # Products
    path('categories/', views.get_categories, name='categories'),
    path('products/', views.get_products, name='products'),
    path('products/<int:pk>/', views.get_product_detail, name='product-detail'),
    
    # Cart
    path('cart/', views.get_cart, name='cart'),
    path('cart/add/', views.add_to_cart, name='cart-add'),
    path('cart/update/<int:item_id>/', views.update_cart_item, name='cart-update'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='cart-remove'),
    path('cart/clear/', views.clear_cart, name='cart-clear'),
    
    # Orders
    path('orders/create/', views.create_order, name='order-create'),
    path('orders/', views.get_user_orders, name='user-orders'),
    path('orders/<str:order_number>/', views.get_order_detail, name='order-detail'),
    
    # Admin endpoints
    path('admin/orders/', views.get_all_orders, name='admin-orders'),
    path('admin/orders/<str:order_number>/', views.update_order_status, name='admin-order-update'),
    path('admin/analytics/', views.get_sales_analytics, name='admin-analytics'),
    path('admin/products/create/', views.create_product, name='admin-product-create'),
    path('admin/products/update/<int:pk>/', views.update_product, name='admin-product-update'),
    path('admin/products/delete/<int:pk>/', views.delete_product, name='admin-product-delete'),
    path('admin/categories/create/', views.create_category, name='admin-category-create'),
    path('admin/categories/update/<int:pk>/', views.update_category, name='admin-category-update'),
    path('admin/categories/delete/<int:pk>/', views.delete_category, name='admin-category-delete'),
    path('admin/users/', views.get_all_users, name='admin-users'),
]