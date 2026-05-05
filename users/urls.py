from django.urls import path
from .views import RegisterView, LoginView, RefreshTokenView, DemoCredentialsView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', RefreshTokenView.as_view(), name='token_refresh'),
    path('demo/', DemoCredentialsView.as_view(), name='demo_credentials'),
]