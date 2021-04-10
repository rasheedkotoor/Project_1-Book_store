from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('otp_login/', views.otp_login, name='otp_login'),
    path('enter_otp/', views.enter_otp, name='enter_otp'),
    path('signup/', views.signup, name='signup'),
    path('signup/<str:ref_code>/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('category/<int:pk>/', views.category, name='category'),
    path('author/<int:pk>/', views.author, name='author'),
    path('book_view/<int:pk>/', views.book_view, name='book_view'),
    path('cart/', views.cart, name='cart'),
    path('add_to_cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('buy_now/<int:pk>/', views.buy_now, name='buy_now'),
    path('delete_cart/<int:pk>/', views.delete_cart, name='delete_cart'),
    path('cart_count/', views.cart_count, name='cart_count'),
    path('checkout/', views.checkout, name='checkout'),
    path('shipping_address/', views.shipping_address, name='shipping_address'),
    path('del_address/<int:pk>/', views.del_address, name='del_address'),
    path('select_address/', views.select_address, name='select_address'),
    path('select_pay_methode/', views.select_pay_methode, name='select_pay_methode'),
    path('order/', views.order, name='order'),
    path('success/', views.success, name='success'),
    path('profile/', views.profile, name='profile'),
    path('profile_pic/', views.profile_pic, name='profile_pic'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('change_password/', views.change_password, name='change_password'),
    path('order_status/', views.order_status, name='order_status'),
    path('add_coupon/', views.add_coupon, name='add_coupon'),
]

