from django.urls import path

from .api import views

app_name = 'orders'

urlpatterns = [
    path('', views.OrderList.as_view(), name='order-list'),
    path('<str:pk>/', views.OrderDetail.as_view(), name='order-detail'),
    path('<str:order_pk>/order-items/', views.OrderItemList.as_view(), name='order-item-list'),
    path('<str:order_pk>/order-items/<str:order_item_pk>/', views.OrderItemDetail.as_view(), name='order-item-detail'),
]
