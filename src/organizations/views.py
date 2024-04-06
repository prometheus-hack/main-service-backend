from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet

from core.permissions import IsAuthorOrReadOnly
from .repositories import CategoryRepository, OrganizationRepository
from .serializers import CategorySerializer, OrganizationListSerializer, OrganizationCreateSerializer


# Create your views here.


class OrganizationViewSet(ModelViewSet):
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthorOrReadOnly]
    queryset = OrganizationRepository.all()

    @method_decorator(vary_on_cookie)
    @method_decorator(cache_page(settings.CACHE_TTL))
    def dispatch(self, request, *args, **kwargs):
        return super(OrganizationViewSet, self).dispatch(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return OrganizationListSerializer
        else:
            return OrganizationCreateSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        serializer.save(owner=self.request.user)


class OrganizationSearchListAPIView(ListAPIView):
    pagination_class = PageNumberPagination
    serializer_class = OrganizationListSerializer

    @method_decorator(vary_on_cookie)
    @method_decorator(cache_page(settings.CACHE_TTL))
    def dispatch(self, request, *args, **kwargs):
        return super(OrganizationSearchListAPIView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        name = self.kwargs.get('name')
        if name:
            return OrganizationRepository.search(name)
        else:
            return OrganizationRepository.all()

    def list(self, request, *args, **kwargs):
        return super().list(request, args, kwargs)


class CategoryListAPIView(ListAPIView):
    pagination_class = PageNumberPagination
    queryset = CategoryRepository.all()
    serializer_class = CategorySerializer


class OrganizationByCategoryListAPIView(ListAPIView):
    pagination_class = PageNumberPagination
    serializer_class = OrganizationListSerializer

    @method_decorator(vary_on_cookie)
    @method_decorator(cache_page(settings.CACHE_TTL))
    def dispatch(self, request, *args, **kwargs):
        return super(OrganizationByCategoryListAPIView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        category = self.kwargs.get('id')
        if category:
            return OrganizationRepository.get_by_category(int(category))
        else:
            return OrganizationRepository.all()
