from rest_framework import serializers


class CartSerializer(serializers.Serializer):

    name = serializers.CharField(max_length=255, required=False, read_only=True)
    product_type_id = serializers.IntegerField()
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()
    price_with_discount = serializers.DecimalField(max_digits=8, decimal_places=2, required=False, read_only=True)
