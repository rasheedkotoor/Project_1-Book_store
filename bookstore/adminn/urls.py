from django.urls import path
from . import views


urlpatterns = [
    path('', views.login, name='login'),
    path('home/', views.home, name='home'),
    path('userlist/', views.userlist, name='userlist'),
    path('category/', views.category, name='category'),
    path('del_cat/<int:pk>/', views.del_cat, name='del_cat'),
    path('block_user/<int:pk>/', views.block_user, name='block_user'),
    path('booklist/', views.booklist, name='booklist'),
    path('add_book/', views.add_book, name='add_book'),
    path('edit_book/<int:pk>/', views.edit_book, name='edit_book'),
    path('delete_book/<int:pk>/', views.delete_book, name='delete_book'),
    path('view_book/<int:pk>/', views.view_book, name='view_book'),
    path('logout/', views.logout, name='logout'),
    path('order_manage/', views.order_manage, name='order_manage'),
    path('admin_order_status/', views.admin_order_status, name='admin_order_status'),
    path('report/', views.report, name='report'),
    path('download_excel_data/', views.download_excel_data, name='download_excel_data'),
    path('add_offer/', views.add_offer, name='add_offer'),
    path('coupon/', views.coupon, name='coupon'),
    # path('end_date/', views.end_date, name='end_date'),


]
