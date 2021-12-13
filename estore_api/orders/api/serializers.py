from rest_framework import serializers
from ..models import *


class OrderItemSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='get_product_name', read_only=True)
    price_with_discount = serializers.CharField(source='get_unit_price', read_only=True)

    class Meta:
        fields = ('id', 'order', 'name', 'item_id', 'item_type', 'quantity', 'price_with_discount')
        model = OrderItem


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(read_only=True, many=True)
    total_cost = serializers.FloatField(source='get_total_cost', read_only=True)

    class Meta:
        fields = (
            'id', 'name', 'surname', 'email', 'address', 'postal_code',
            'city', 'created', 'order_items', 'total_cost'
        )
        model = Order
