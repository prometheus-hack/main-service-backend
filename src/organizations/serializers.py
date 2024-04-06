from rest_framework import serializers

from core.fields import LocationField
from jwtauth.serializers import CustomUserSerializer
from .models import Category, Location, Organization, OrganizationImage
from .repositories import OrganizationImagesRepository, CategoryRepository


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class LocationSerializer(serializers.ModelSerializer):
    coords = LocationField()
    region = serializers.StringRelatedField()

    class Meta:
        model = Location
        fields = ('pk', 'coords', 'region', 'address')


class OrganizationListSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    images = serializers.StringRelatedField(source='organization_images', many=True)

    class Meta:
        model = Organization
        fields = ('location', 'images', 'name', 'phone', 'description', 'website', 'category')


class OrganizationCreateSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    images = serializers.PrimaryKeyRelatedField(source='organization_images', many=True, queryset=OrganizationImagesRepository)
    owner = serializers.StringRelatedField()
    category = serializers.PrimaryKeyRelatedField(queryset=CategoryRepository.all())

    class Meta:
        model = Organization
        fields = ('location', 'images', 'name', 'phone', 'website', 'description', 'owner', 'category')
