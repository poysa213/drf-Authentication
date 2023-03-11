from django.urls import path


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import RegisterView, ChangePasswordView,  AuthTest, SendOTPView, ResetPasswordView



urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', RegisterView.as_view(), name='register_user'),
    path('api/change-password/', ChangePasswordView.as_view(), name='auth_change_password'),
    path('api/test/' , AuthTest.as_view(), name="hello"),
    path('api/send-otp/', SendOTPView.as_view(), name='send-otp'),
    path('api/reset-password/', ResetPasswordView.as_view(), name='reset-password')
]

