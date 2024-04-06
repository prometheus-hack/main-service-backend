from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from core.permissions import IsAuthorOrReadOnly
from organizations.repositories import OrganizationRepository
from .repositories import PhotoRepository, FavouriteOrganizationRepository
from .serializers import PhotoSerializer, ListPhotoSerializer, FavouriteOrganizationSerializer

# Create your views here.


class PhotoListCreateAPIView(ListAPIView, CreateAPIView):
    queryset = PhotoRepository.all()
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthorOrReadOnly]

    def get_serializer_class(self):
        if self.request.POST:
            return PhotoSerializer
        else:
            return ListPhotoSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FavouriteOrganizationAPIView(CreateAPIView, DestroyAPIView):
    serializer_class = FavouriteOrganizationSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user=self.request.user, organization__pk=self.kwargs.get('id'))
        return obj

    def perform_create(self, serializer):
        if FavouriteOrganizationRepository.get_filtered(user=self.request.user, organization=OrganizationRepository.get(
                self.kwargs.get('id'))):
            pass
        else:
            serializer.save(user=self.request.user, organization=self.kwargs.get('id'))


class FavouriteOrganizationsListAPIView(ListAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    serializer_class = FavouriteOrganizationSerializer

    def get_queryset(self):
        return FavouriteOrganizationRepository.get_filtered(user=self.request.user)
