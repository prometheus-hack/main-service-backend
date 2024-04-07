from django.conf import settings
from django.db import models

# Create your models here.


class OrganizationAccount(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    organization = models.ForeignKey('organizations.Organization', on_delete=models.CASCADE)


class QRCodeUsing(models.Model):
    organization = models.ForeignKey('organizations.Organization', on_delete=models.CASCADE)
    used_dt = models.DateTimeField(auto_now=True)
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, default=None)
