from rest_framework import serializers
from ..models import *


class OrderItemSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='get_product_name', read_only=True)
    price_with_discount = serializers.CharField(source='get_unit_price', read_only=True)

    class Meta:
        fields = ('id', 'order', 'name', 'item_id', 'item_type', 'quantity', 'price_with_discount')
        model = OrderItem


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Order


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = OrderItem
