from rest_framework import serializers

from organizations.repositories import OrganizationRepository
from .models import Bonus, FavouriteOrganization, Photo


class PhotoSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = Photo
        fields = ('image', 'user')


class ListPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        fields = ('image',)


class FavouriteOrganizationSerializer(serializers.ModelSerializer):
    organization = serializers.PrimaryKeyRelatedField(queryset=OrganizationRepository.all(), read_only=False)
    user = serializers.StringRelatedField()

    class Meta:
        model = FavouriteOrganization
        fields = ('organization', 'user')
