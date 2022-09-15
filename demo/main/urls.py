from .import views
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [
    path('register/', views.RegistrationView.as_view(), name="register"),
    path('verify-email/', views.EmailVerificationView.as_view(), name = "verify-email"),
    path('resend-verification-email/', views.ResendVerificationEmailView.as_view(), name = "resend-verification-email"),
    path('login/', views.LoginView.as_view(), name="login"),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh')

 ]  
