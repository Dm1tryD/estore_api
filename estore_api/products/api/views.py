from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.filters import SearchFilter, OrderingFilter

from ..models import Notebook, Phone
from .serializers import NotebookSerializer, PhoneSerializer


class MixinTechModelViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, permissions.DjangoModelPermissionsOrAnonReadOnly,)
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['category', 'available', 'price', 'cpu', 'gpu']
    search_fields = ['name', 'brand']
    ordering_fields = ['priority']


class PhoneViewSet(MixinTechModelViewSet):
    queryset = Phone.objects.all()
    serializer_class = PhoneSerializer


class NotebookViewSet(MixinTechModelViewSet):
    queryset = Notebook.objects.all()
    serializer_class = NotebookSerializer
