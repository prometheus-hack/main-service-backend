from core.repositories import BaseRepository
from .models import Photo, FavouriteOrganization


class PhotoRepository(BaseRepository):
    model = Photo


class FavouriteOrganizationRepository(BaseRepository):
    model = FavouriteOrganization

    @classmethod
    def get_filtered(cls, **kwargs):
        return cls.model.objects.filter(**kwargs)
