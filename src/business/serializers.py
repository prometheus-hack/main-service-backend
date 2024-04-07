from datetime import datetime, time
from django.conf import settings
from rest_framework import serializers
from pytz import timezone

from .models import QRCodeUsing, OrganizationAccount
from .repositories import QRCodeUsingRepository


class ListUsingQRCodeSerializer(serializers.Serializer):
    date = serializers.SerializerMethodField(method_name='get_timestamp', read_only=True)
    scansCount = serializers.SerializerMethodField(method_name='get_scans_count', read_only=True)

    def get_timestamp(self, obj):
        return datetime.combine(obj['date'], time=time(), tzinfo=timezone(settings.TIME_ZONE)).timestamp()

    def get_scans_count(self, obj):
        pk = int(''.join([i for i in self.context['request'].path if i.isdigit()]))
        return QRCodeUsingRepository.count(pk, self.get_timestamp(obj))


class DetailedUsingQRCodeSerializer(serializers.ModelSerializer):

    timestamp = serializers.SerializerMethodField(method_name='get_timestamp', read_only=True)
    user = serializers.StringRelatedField(source='client', read_only=True)
    discountPercent = serializers.IntegerField(source='discount')

    class Meta:
        model = QRCodeUsing
        fields = ('id', 'user', 'organization_id', 'timestamp')

    def get_timestamp(self, obj):
        return obj.used_dt.timestamp()


class OrganizationAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationAccount
        fields = ('user', 'organization')
