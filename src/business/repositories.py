from datetime import datetime, timedelta

from django.db.models.functions import TruncDate

from core.repositories import BaseRepository, ObjectDoesNotExist
from .models import OrganizationAccount, QRCodeUsing


class OrganizationAccountRepository(BaseRepository):
    model = OrganizationAccount

    @classmethod
    def get(cls, **kwargs):
        try:
            return cls.model.objects.get(**kwargs)
        except ObjectDoesNotExist:
            return None

    @classmethod
    def filter_by_organization(cls, organization_id):
        return cls.model.objects.filter(organization__id=organization_id)

    @classmethod
    def none(cls):
        return cls.model.objects.none()


class QRCodeUsingRepository(BaseRepository):
    model = QRCodeUsing

    @staticmethod
    def __get_dates_from_timestamp(timestamp):
        return datetime.fromtimestamp(timestamp).date(), datetime.fromtimestamp(timestamp).date() + timedelta(days=1)

    @classmethod
    def get_by_timestamp(cls, organization_id, timestamp):
        start_date, end_date = cls.__get_dates_from_timestamp(timestamp)
        return cls.model.objects.filter(organization__pk=organization_id, used_dt__gte=start_date,
                                        used_dt__lt=end_date)

    @classmethod
    def get_with_dates(cls, organization_id):
        return cls.model.objects.filter(organization__pk=organization_id).values(date=TruncDate('used_dt')).distinct()

    @classmethod
    def count(cls, organization_id, timestamp):
        start_date, end_date = cls.__get_dates_from_timestamp(timestamp)
        return cls.model.objects.filter(organization__pk=organization_id, used_dt__gte=start_date,
                                        used_dt__lt=end_date).count()
