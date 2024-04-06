from .models import Category, Location, Organization, OrganizationImage, Region
from core.repositories import BaseRepository


class CategoryRepository(BaseRepository):
    model = Category

    @classmethod
    def get_by_name(cls, name):
        return cls.model.objects.get(name=name)


class LocationRepository(BaseRepository):
    model = Location

    @classmethod
    def get_or_create(cls, coords, address, region=None):
        if region is None:
            region = 23
        if Location.objects.get(coords=coords):
            return Location.objects.get(coords=coords)
        else:
            obj = LocationRepository.create(
                coords=coords,
                region=region,
                address=address
            )
            return obj


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
