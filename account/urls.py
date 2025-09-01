from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)
from account.views import RegisterView, VerifyEmailView,UserLoginView, UserLogoutView, UserUpdateView, PasswordChangeView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('verify-email/', VerifyEmailView.as_view(), name='verify-email'),
    path('token/refresh/', TokenRefreshView.as_view(), name="token_refresh"),
    path('update/', UserUpdateView.as_view(), name='user_update'),
    path('change-password/', PasswordChangeView.as_view(), name='change_password'),
]
