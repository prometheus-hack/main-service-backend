from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import RegistrationAPIView, LoginAPIView, CustomUserRetrieveUpdateAPIView, RefreshAPIView, ProfileRetrieveUpdateDestroyAPIView, ProfileRetrieveAPIView, ProfileListAPIView

app_name = 'jwtauth'

urlpatterns = [
    path('registration/', RegistrationAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('refresh/', RefreshAPIView.as_view()),
    path('profile/<int:id>', ProfileRetrieveAPIView.as_view()),
    path('profiles/', ProfileListAPIView.as_view()),
    path('profile/', ProfileRetrieveUpdateDestroyAPIView.as_view()),
    path('', CustomUserRetrieveUpdateAPIView.as_view()),
]
