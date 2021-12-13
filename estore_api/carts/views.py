from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .api.serializers import CartSerializer
from .cart import Cart


class CartItemDetail(APIView):

    def put(self, request, product_type_id, product_id):
        """
        Change the quantity of the product
        """
        quantity = request.data['quantity']
        cart = Cart(request, product_type_id, product_id)
        data = {
            "product_type_id": product_type_id,
            "product_id": product_id,
            "quantity": quantity,
        }
        cart.update(quantity)
        return Response(data)

    def delete(self, request, product_type_id, product_id):
        """
        Remove a product from cart
        """
        cart = Cart(request, product_type_id, product_id)
        cart.delete()
        return Response({'success': 'Delete success'})


class ListCartItems(ListCreateAPIView):

    serializer_class = CartSerializer

    def get(self, request, *args, **kwargs):
        """
        Get all the products in the basket of the current session
        """
        try:
            cart = request.session[settings.CART_SESSION_ID]
            return Response(cart)
        except KeyError:
            return Response('Card is not initialized')

    def post(self, request, *args, **kwargs):
        """
        Add product to cart
        """
        cart_serializer = CartSerializer(data=request.data)
        if cart_serializer.is_valid():
            product_type_id = cart_serializer.data['product_type_id']
            product_id = cart_serializer.data['product_id']
            quantity = cart_serializer.data['quantity']
            product = get_object_or_404(get_object_or_404(ContentType, pk=product_type_id).model_class(), pk=product_id)
            if product:
                data = {
                    "name": product.name,
                    "product_type_id": product_type_id,
                    "product_id": product_id,
                    "price_with_discount": str(product.get_price_with_discount),
                    "quantity": quantity,
                }
                cart = Cart(request, product_type_id, product_id, product)
                cart.add(quantity)
                return Response(data)
            return Response({'error': 'Product doesn\'t exist'})
        return Response(cart_serializer.errors)
