from .models import Category, Location, Organization, OrganizationImage, Region
from core.repositories import BaseRepository


class CategoryRepository(BaseRepository):
    model = Category


class LocationRepository(BaseRepository):
    model = Location


class OrganizationRepository(BaseRepository):
    model = Organization

    @classmethod
    def search(cls, name):
        return cls.model.objects.filter(name__icontains=name)

    @classmethod
    def get_by_category(cls, category_id):
        return cls.model.objects.filter(category__pk=category_id)


class OrganizationImagesRepository(BaseRepository):
    model = OrganizationImage


class RegionRepository(BaseRepository):
    model = Region
