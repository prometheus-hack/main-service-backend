from django.db import models
from django.contrib.gis.db.models import PointField

# Create your models here.


class Region(models.Model):
    code = models.PositiveIntegerField()
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Location(models.Model):
    coords = PointField(db_index=True)
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=512, blank=True, null=True)

    def __str__(self):
        return str(self.coords)


class Category(models.Model):
    name = models.CharField(max_length=64)
    icon = models.ImageField(upload_to='icons/category/')

    def __str__(self):
        return self.name


class Organization(models.Model):
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=256, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, default=None)
    website = models.URLField(blank=True)
    description = models.TextField(blank=True)
    owner = models.ForeignKey('jwtauth.CustomUser', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class OrganizationImage(models.Model):
    image = models.ImageField(upload_to='images/organizations')
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='organization_images')
