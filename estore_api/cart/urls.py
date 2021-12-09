from django.urls import path

from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.ListCartItems.as_view(), name='cart-detail'),
    path('<str:product_type_id>/<str:product_id>/', views.CartItemDetail.as_view(), name='cart-item-detail'),
]
