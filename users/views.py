from django.db import IntegrityError
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.utils import extend_schema
from .signals import ensure_demo_user
from .serializers import (
    UserSerializer,
    RegisterRequestSerializer,
    UserResponseSerializer,
    TokenPairSerializer,
    TokenRefreshOutputSerializer,
    LoginRequestSerializer,
    TokenRefreshRequestSerializer,
)


class RegisterView(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

    @extend_schema(
        tags=['Authentication'],
        operation_id='auth_register',
        summary='Register a new user',
        request=RegisterRequestSerializer,
        responses={201: UserResponseSerializer},
        auth=[],
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save()
        except IntegrityError:
            return Response(
                {"detail": "A user with that username already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception:
            return Response(
                {"detail": "Unable to create user. Please check the submitted data."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {
                "id": serializer.instance.id,
                "username": serializer.instance.username,
                "email": serializer.instance.email,
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]
    authentication_classes = []

    @extend_schema(
        tags=['Authentication'],
        operation_id='auth_login',
        summary='Obtain access and refresh tokens',
        request=LoginRequestSerializer,
        responses=TokenPairSerializer,
        auth=[],
    )
    def post(self, request, *args, **kwargs):
        ensure_demo_user()
        return super().post(request, *args, **kwargs)


class RefreshTokenView(TokenRefreshView):
    permission_classes = [AllowAny]
    authentication_classes = []

    @extend_schema(
        tags=['Authentication'],
        operation_id='auth_refresh',
        summary='Refresh the access token',
        request=TokenRefreshRequestSerializer,
        responses=TokenRefreshOutputSerializer,
        auth=[],
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
