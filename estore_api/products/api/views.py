from rest_framework import viewsets
from rest_framework import permissions

from ..models import Notebook, Phone
from .serializers import NotebookSerializer, PhoneSerializer


class NotebookViewSet(viewsets.ModelViewSet):
    queryset = Notebook.objects.all()
    serializer_class = NotebookSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return super(self.__class__, self).get_permissions()
        return [permissions.IsAdminUser()]


class PhoneViewSet(viewsets.ModelViewSet):
    queryset = Phone.objects.all()
    serializer_class = PhoneSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return super(self.__class__, self).get_permissions()
        return [permissions.IsAdminUser()]
