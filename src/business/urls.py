from django.urls import path

from .views import *


urlpatterns = [
    path('organizations/accounts/<int:id>/', OrganizationAccountDestroyAPIView.as_view()),
    path('organization/<int:id>/accounts/', OrganizationAccountsListAPIView.as_view()),
    path('organization/<int:id>/accounts/', OrganizationAccountCreateAPIView.as_view()),
    path('organization/<int:id>/scans/<int:timestamp>/', QRCodeUsingDetailedListAPIView.as_view()),
    path('organization/<int:id>/scans/', QRCodeUsingListAPIView.as_view()),
    path('qr-code/check/', QrCodeProveAPIView.as_view()),
]