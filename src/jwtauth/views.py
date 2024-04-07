from datetime import datetime

from django.conf import settings
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from pytz import timezone
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView, CreateAPIView, ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from core.permissions import IsAuthorOrReadOnly
from .models import CustomUser, RefreshToken
from .repositories import RefreshTokenRepository, ProfileRepository, UserRepository, QRCodeRepository
from .serializers import RegistrationSerializer, LoginSerializer, CustomUserSerializer, ProfileSerializer, QRCodeSerializer
from .renderers import CustomUserJSONRenderer
from .token_generators import generate_rt, generate_jwt


# Create your views here.


class RefreshAPIView(APIView):
    """
    Refreshing old access token
    """
    permission_classes = (AllowAny,)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'refresh_token': openapi.Schema(type=openapi.TYPE_STRING, description='refresh_token'),
        },
        required=['refresh_token']
    ),
        responses={
            status.HTTP_200_OK: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'access_token': openapi.Schema(type=openapi.TYPE_STRING),
                    'refresh_token': openapi.Schema(type=openapi.TYPE_STRING)
                }
            ),
        }
    )
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')
            old_token = RefreshTokenRepository.get(token=refresh_token)
            user = old_token.user
        except RefreshToken.DoesNotExist:
            return Response({
                'error': 'Token is not valid'
            }, status=status.HTTP_400_BAD_REQUEST)
        if not old_token.used and old_token.expires > datetime.now(tz=timezone(settings.TIME_ZONE)):
            token = RefreshToken.objects.create(
                token=generate_rt(),
                user=user
            )
            old_token.delete()
            data = {
                'access_token': generate_jwt(user.pk),
                'refresh_token': token.token
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(
                data={
                    'error': 'Token expired',
                },
                status=status.HTTP_400_BAD_REQUEST
            )


class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer
    renderer_classes = (CustomUserJSONRenderer,)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='email'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='user password')
        }
    ),
        responses={
            status.HTTP_200_OK: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'email': openapi.Schema(type=openapi.TYPE_STRING),
                    'access_token': openapi.Schema(type=openapi.TYPE_STRING),
                    'refresh_token': openapi.Schema(type=openapi.TYPE_STRING)
                }
            ),
        }
    )
    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        ProfileRepository.create(user=UserRepository.get(serializer.data['email']))
        QRCodeRepository.create(user=UserRepository.get(serializer.data['email']))
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    renderer_classes = (CustomUserJSONRenderer,)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'email': openapi.Schema(type=openapi.TYPE_STRING, description='email'),
            'password': openapi.Schema(type=openapi.TYPE_STRING, description='user password')
        },
    ),
        responses={
            status.HTTP_200_OK: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'email': openapi.Schema(type=openapi.TYPE_STRING),
                    'access_token': openapi.Schema(type=openapi.TYPE_STRING),
                    'refresh_token': openapi.Schema(type=openapi.TYPE_STRING)
                }
            ),
        }
    )
    def post(self, request):
        user = request.data

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class CustomUserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (CustomUserJSONRenderer,)
    serializer_class = CustomUserSerializer

    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer_data = request.data
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


# class ChangePasswordAPIView(APIView):
#
#     permission_classes = (IsAuthenticated,)
#
#     @swagger_auto_schema(request_body=openapi.Schema(
#         type=openapi.TYPE_OBJECT,
#         properties={
#             'new_password': openapi.Schema(type=openapi.TYPE_STRING, description='refresh_token'),
#         },
#         required=['new_password']
#     ),
#         responses={
#             status.HTTP_200_OK: openapi.Schema(
#                 type=openapi.TYPE_OBJECT,
#                 properties={
#                     'message': 'password changed',
#                 }
#             ),
#             status.HTTP_401_UN
#         }
#     )
#     def post(self, request):
#         pass


class ProfileRetrieveUpdateDestroyAPIView(CreateAPIView, RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer
    queryset = ProfileRepository.all()

    def get_queryset(self):
        return self.queryset

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user=self.request.user)
        return obj

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class ProfileRetrieveAPIView(RetrieveAPIView):
    permission_classes = (IsAuthorOrReadOnly,)
    serializer_class = ProfileSerializer
    queryset = ProfileRepository.all()


class ProfileListAPIView(ListAPIView):
    queryset = ProfileRepository.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAdminUser]
    pagination_class = PageNumberPagination


class QRCodeRetrieveAPIView(RetrieveAPIView):
    serializer_class = QRCodeSerializer
    queryset = QRCodeRepository.all()

    def get_object(self):
        return QRCodeRepository.get(self.request.user)
