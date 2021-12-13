from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

User = get_user_model()


class Order(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=24)
    surname = models.CharField(max_length=24)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return f'Order {self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    item_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, limit_choices_to={"model__istartswith": settings.MODEL_START_WORD}
    )
    item_id = models.PositiveIntegerField()
    product = GenericForeignKey('item_type', 'item_id')
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.product)

    def get_unit_price(self):
        return self.product.price

    def get_cost(self):
        return self.product.price * self.quantity
