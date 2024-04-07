from django.contrib.gis.geos import Polygon

from .models import Category, Location, Organization, OrganizationImage, Region
from core.repositories import BaseRepository, ObjectDoesNotExist


class CategoryRepository(BaseRepository):
    model = Category

    @classmethod
    def get_by_name(cls, name):
        return cls.model.objects.get(name=name)


class LocationRepository(BaseRepository):
    model = Location

    @classmethod
    def get_or_create(cls, coords, address):
        region, _ = Region.objects.get_or_create(code=23)
        try:
            return Location.objects.get(coords=coords)
        except ObjectDoesNotExist:
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

    @classmethod
    def get_by_categories(cls, categories):
        return cls.model.objects.filter(category__pk__in=categories)

    @classmethod
    def get_for_map(cls, categories, coords1, coords2):
        rectangle = Polygon.from_bbox((*coords1, *coords2))
        return cls.get_by_categories(categories).filter(location__coords__within=rectangle)

    @classmethod
    def get_by_owner(cls, owner):
        return cls.model.objects.filter(owner=owner)


class OrganizationImagesRepository(BaseRepository):
    model = OrganizationImage


class RegionRepository(BaseRepository):
    model = Region
