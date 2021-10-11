from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from estore_api.users.api.views import RegisterView, ChangePasswordView, UpdateProfileView, LogoutView, \
    LogoutAllView, RequestPasswordResetEmail, PasswordTokenCheckAPI, SetNewPasswordAPIView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='user-register'),

    path('login/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),

    path('request-reset-email/', RequestPasswordResetEmail.as_view(), name="request-reset-email"),
    path('password-reset/<uidb64>/<token>/', PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('password-reset-complete', SetNewPasswordAPIView.as_view(), name='password-reset-complete'),

    path('change-password/<int:pk>/', ChangePasswordView.as_view(), name='user-change-password'),

    path('update-profile/<int:pk>/', UpdateProfileView.as_view(), name='user-update-profile'),
    path('update-profile/<int:pk>/', UpdateProfileView.as_view(), name='user-update-profile'),
    path('logout/', LogoutView.as_view(), name='user-logout'),
    path('logout-all/', LogoutAllView.as_view(), name='user-logout-all'),
]
