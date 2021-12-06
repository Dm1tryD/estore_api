from django.urls import path
from rest_framework import routers

from .api.views import LaptopViewSet, PhoneViewSet

router = routers.SimpleRouter()
router.register(r'laptop', LaptopViewSet)
router.register(r'phone', PhoneViewSet)

urlpatterns = []
urlpatterns += router.urls
