from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response

from ..models import Order, OrderItem
from .. import tasks
from .serializers import OrderSerializer, OrderItemSerializer


class OrderList(ListCreateAPIView):

    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        if self.request.user:
            serializer.validated_data['user'] = self.request.user
            serializer.save()

    @staticmethod
    def is_in_stock(product, quantity):
        if quantity > product.stock:
            return False
        return True

    def add_cart_items_to_order(self, order, cart_items):
        """
        Add cart items to order if at least one item with an error return an error
        """
        for cart_item in cart_items:
            product_type_id = cart_item['product_type']
            product_id = cart_item['product_id']
            quantity = cart_item['quantity']
            data = {
                'order': order.id,
                'item_type': product_type_id,
                'item_id': product_id,
                'quantity': quantity
            }
            product_serializer = OrderItemSerializer(data=data)
            product = get_object_or_404(get_object_or_404(ContentType, pk=product_type_id).model_class(), pk=product_id)
            if product_serializer.is_valid():
                if self.is_in_stock(product, quantity):
                    product_serializer.save()
                else:
                    return {'error': f'Product {product_type_id}_{product_id} is not enough'}
            else:
                return {'error': product_serializer.errors}
        return {'success': True}

    def post(self, request, *args, **kwargs):
        """
        Create an order and add items from the cart to it
        """
        order_serializer = OrderSerializer(data=request.data)
        if order_serializer.is_valid():
            order = order_serializer.save()
            cart_items = request.session[settings.CART_SESSION_ID].values()
            if cart_items:
                products_in_order = self.add_cart_items_to_order(order, cart_items)
                if 'success' in products_in_order:
                    del request.session[settings.CART_SESSION_ID]
                    tasks.send_order_email(
                        order
                    )
                    return Response('Order was successfully created')
                order.delete()
                return Response(products_in_order['error'])
            return Response('Cart is empty')
        return Response(order_serializer.errors)


class OrderDetail(RetrieveUpdateDestroyAPIView):

    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class OrderItemList(ListCreateAPIView):

    serializer_class = OrderItemSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        return OrderItem.objects.filter(order__pk=self.kwargs['order_pk'])


class OrderItemDetail(RetrieveUpdateDestroyAPIView):

    serializer_class = OrderItemSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_object(self):
        return OrderItem.objects.get(pk=self.kwargs['order_item_pk'])
