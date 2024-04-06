from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import OrganizationViewSet, OrganizationSearchListAPIView, OrganizationByCategoryListAPIView, CategoryListAPIView, OrganizationMapFilterAPIView, UploadAPIView

app_name = "organizations"

router = DefaultRouter()
router.register('', OrganizationViewSet, 'organizations')
urlpatterns = [
    path('category/<int:id>/organizations/', OrganizationByCategoryListAPIView.as_view()),
    path('search/<str:name>/', OrganizationSearchListAPIView.as_view()),
    path('categories/', CategoryListAPIView.as_view()),
    path('map/', OrganizationMapFilterAPIView.as_view())
    # path('upload/', UploadAPIView.as_view())
] + router.urls
