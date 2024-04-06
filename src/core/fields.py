from django.contrib.gis.geos.point import Point
from rest_framework import serializers


class LocationField(serializers.Field):
    default_error_messages = {
        "invalid": "Value must be valid list with lang and lat values."
    }

    def to_representation(self, value):
        return value.coords

    def to_internal_value(self, data):
        try:
            point = Point((data[0], data[1]))
        except Exception:
            self.fail("invalid")

        return point