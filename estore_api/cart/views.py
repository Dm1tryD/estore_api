from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .cart import Cart


class CartItemDetail(APIView):

    def put(self, request, product_type_id, product_id):
        """
        Change the quantity of the product
        """
        quantity = request.data['quantity']
        cart = Cart(request, product_type_id, product_id)
        unique_product_identifier = str(product_type_id) + '_' + str(product_id)
        price = self.request.session[settings.CART_SESSION_ID][unique_product_identifier]['price']
        data = {
            "product_id": product_id,
            "product_type": product_type_id,
            "price": price,
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
        return Response('Delete success')


class ListCartItems(APIView):

    def get(self, request):
        """
        Get all the products in the basket of the current session
        """
        try:
            cart = request.session[settings.CART_SESSION_ID]
            return Response(cart)
        except KeyError:
            return Response('Cart is empty')

    def post(self, request):
        """
        Add product to cart
        """
        try:
            product_type_id = request.data['product_type_id']
            product_id = request.data['product_id']
            quantity = request.data['quantity']
        except KeyError as e:
            return Response(f'Error argument {e} was not found.')
        product = get_object_or_404(get_object_or_404(ContentType, pk=product_type_id).model_class(), pk=product_id)
        if product:
            data = {
                "product_id": product_id,
                "product_type": product_type_id,
                "price": str(product.price),
                "quantity": quantity,
            }
            cart = Cart(request, product_type_id, product_id, product)
            cart.add(quantity)
            return Response(data)
