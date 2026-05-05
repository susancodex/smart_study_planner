from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.utils import extend_schema
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    TokenPairSerializer,
    TokenRefreshSerializer,
    TokenRefreshOutputSerializer,
)


class RegisterView(generics.GenericAPIView):
    """Register a new user account."""

    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

    @extend_schema(
        tags=['Authentication'],
        operation_id='auth_register',
        summary='Register a new user',
        auth=[],
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginView(TokenObtainPairView):
    """Login with username and password to receive JWT tokens."""

    permission_classes = [AllowAny]
    authentication_classes = []

    @extend_schema(
        tags=['Authentication'],
        operation_id='auth_login',
        summary='Login and get access + refresh tokens',
        request=LoginSerializer,
        responses=TokenPairSerializer,
        auth=[],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class RefreshTokenView(TokenRefreshView):
    """Exchange a refresh token for a new access token."""

    permission_classes = [AllowAny]
    authentication_classes = []

    @extend_schema(
        tags=['Authentication'],
        operation_id='auth_refresh',
        summary='Refresh the access token',
        request=TokenRefreshSerializer,
        responses=TokenRefreshOutputSerializer,
        auth=[],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
