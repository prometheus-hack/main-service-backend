from django.urls import path

from .views import PhotoListCreateAPIView, FavouriteOrganizationAPIView, FavouriteOrganizationsListAPIView


urlpatterns = [
    path('gallery/', PhotoListCreateAPIView.as_view()),
    path('wishlist/<int:id>/favourite/', FavouriteOrganizationAPIView.as_view()),
    path('wishlist/', FavouriteOrganizationsListAPIView.as_view())
]
