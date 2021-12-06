from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.filters import SearchFilter, OrderingFilter

from ..models import ProductTypeLaptop, ProductTypePhone
from .serializers import LaptopSerializer, PhoneSerializer


class MixinTechModelViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, permissions.DjangoModelPermissionsOrAnonReadOnly,)
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['category', 'available', 'price', 'cpu', 'gpu']
    search_fields = ['name', 'brand']
    ordering_fields = ['priority']


class PhoneViewSet(MixinTechModelViewSet):
    queryset = ProductTypePhone.objects.all()
    serializer_class = PhoneSerializer


class LaptopViewSet(MixinTechModelViewSet):
    queryset = ProductTypeLaptop.objects.all()
    serializer_class = LaptopSerializer
