from django.urls import path

from .views import PhotoListCreateAPIView, FavouriteOrganizationAPIView


urlpatterns = [
    path('gallery/', PhotoListCreateAPIView.as_view()),
    path('wishlist/', FavouriteOrganizationAPIView.as_view())
]
