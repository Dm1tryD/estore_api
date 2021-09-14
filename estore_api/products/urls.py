from django.urls import path
from rest_framework import routers

from .api.views import NotebookViewSet, PhoneViewSet

router = routers.SimpleRouter()
router.register(r'notebook', NotebookViewSet)
router.register(r'phone', PhoneViewSet)

urlpatterns = []
urlpatterns += router.urls
