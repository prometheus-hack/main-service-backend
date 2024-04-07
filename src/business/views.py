from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.permissions import IsOrganizationOwner
from .repositories import QRCodeUsingRepository, OrganizationAccountRepository
from .serializers import DetailedUsingQRCodeSerializer, ListUsingQRCodeSerializer, OrganizationAccountSerializer
from .services import qr_prove

# Create your views here.


class QRCodeUsingListAPIView(ListAPIView):
    pagination_class = PageNumberPagination
    serializer_class = ListUsingQRCodeSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return QRCodeUsingRepository.get_with_dates(self.kwargs.get('id'))


class QRCodeUsingDetailedListAPIView(ListAPIView):
    pagination_class = PageNumberPagination
    serializer_class = DetailedUsingQRCodeSerializer
    lookup_field = 'id'

    def get_queryset(self):
        return QRCodeUsingRepository.get_by_timestamp(self.kwargs.get('id'), int(self.kwargs.get('timestamp')))


class QrCodeProveAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'qrCodeData': openapi.Schema(type=openapi.TYPE_STRING, description='access_token'),
        },
        required=['qrCodeData']
    ),
        responses={
            status.HTTP_200_OK: openapi.Schema(
                type=openapi.TYPE_OBJECT
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Schema(
                type=openapi.TYPE_OBJECT
            ),
            status.HTTP_403_FORBIDDEN: openapi.Schema(
                type=openapi.TYPE_OBJECT
            )
        }
    )
    def post(self, request):
        self.check_permissions(request)
        oa = OrganizationAccountRepository.get(user=self.request.user)
        if oa:
            try:
                client = qr_prove(self.request.data['qrCodeData'])
            except KeyError:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            if client:
                QRCodeUsingRepository.create(
                    organization_id=oa.organization.pk,
                    client=client
                )
                return Response(status=status.HTTP_200_OK)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_403_FORBIDDEN)


class OrganizationAccountCreateAPIView(CreateAPIView):
    serializer_class = OrganizationAccountSerializer
    permission_classes = [IsOrganizationOwner]
    queryset = OrganizationAccountRepository.all()


class OrganizationAccountDestroyAPIView(DestroyAPIView):
    serializer_class = OrganizationAccountSerializer
    permission_classes = [IsOrganizationOwner]
    queryset = OrganizationAccountRepository.all()


class OrganizationAccountsListAPIView(ListAPIView):
    serializer_class = OrganizationAccountSerializer
    permission_classes = [IsOrganizationOwner]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        pk = self.kwargs.get('id')
        if pk:
            return OrganizationAccountRepository.filter_by_organization(int(pk))
        else:
            return OrganizationAccountRepository.none()
