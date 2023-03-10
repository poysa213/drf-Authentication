from django.urls import path


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import RegisterView, ChangePasswordView,  AuthTest



urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', RegisterView.as_view(), name='register_user'),
    path('api/change_password/', ChangePasswordView.as_view(), name='auth_change_password'),
    # path('api/profile/', ProfileView.as_view(), name="profile-name"),
    path('api/test/' , AuthTest.as_view(), name="hello")
]

