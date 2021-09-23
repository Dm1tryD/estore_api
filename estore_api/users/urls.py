from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from estore_api.users.api.views import RegisterView, ChangePasswordView, UpdateProfileView, LogoutView, \
    LogoutAllView

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('register/', RegisterView.as_view(), name='user-register'),
    path('change-password/<int:pk>/', ChangePasswordView.as_view(), name='user-change-password'),
    path('update-profile/<int:pk>/', UpdateProfileView.as_view(), name='user-update-profile'),
    path('logout/', LogoutView.as_view(), name='user-logout'),
    path('logout_all/', LogoutAllView.as_view(), name='user-logout-all'),
]
