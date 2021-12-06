from rest_framework import serializers
from ..models import *


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Order


class OrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = OrderItem
