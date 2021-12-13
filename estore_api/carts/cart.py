from decimal import Decimal

from django.conf import settings


class Cart:
    """
    A base cart class, providing some default behaviors that
    can be inherited or overrided, as necessary.
    """

    def __init__(self, request, product_type_id, product_id, product=None):
        self.session = request.session
        self.product = product
        self.product_type_id = product_type_id
        self.product_id = product_id
        self.unique_product_identifier = str(product_type_id) + '_' + str(product_id)

        cart = self.session.get(settings.CART_SESSION_ID)
        if settings.CART_SESSION_ID not in request.session:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __len__(self):
        """
        Get the cart data and count the quantity of items
        """
        return sum(item["quantity"] for item in self.cart.values())

    def get_subtotal_price(self):
        return sum(Decimal(item["price_with_discount"]) * item["qty"] for item in self.cart.values())

    def add(self, quantity):
        """
        Adding and updating the users cart session data
        """

        if self.unique_product_identifier in self.cart:
            self.cart[self.unique_product_identifier]["quantity"] = quantity
        else:
            self.cart[self.unique_product_identifier] = {
                "name": str(self.product.name),
                "product_id": self.product_id,
                "product_type": self.product_type_id,
                "price_with_discount": str(self.product.get_price_with_discount()),
                "quantity": quantity,
            }

        self.save()

    def save(self):
        self.session.modified = True

    def update(self, quantity):
        """
        Update values in session data
        """
        if self.unique_product_identifier in self.cart:
            self.cart[self.unique_product_identifier]["quantity"] = int(quantity)
        self.save()

    def delete(self):
        """
        Delete item from session data
        """
        if self.unique_product_identifier in self.cart:
            del self.cart[self.unique_product_identifier]
            self.save()

    def clear(self):
        # Remove cart from session
        del self.session[settings.CART_SESSION_ID]
        self.save()
