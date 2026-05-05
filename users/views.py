from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.utils import extend_schema
from .serializers import UserSerializer

class RegisterView(generics.GenericAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

    @extend_schema(
        tags=['Authentication'],
        operation_id='auth_register',
        summary='Register a new user',
        request=UserSerializer,
        responses=UserSerializer,
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]
    authentication_classes = []

    @extend_schema(tags=['Authentication'], operation_id='auth_login', summary='Obtain access and refresh tokens')
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class RefreshTokenView(TokenRefreshView):
    permission_classes = [AllowAny]
    authentication_classes = []

    @extend_schema(tags=['Authentication'], operation_id='auth_refresh', summary='Refresh the access token')
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)