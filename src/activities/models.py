from django.conf import settings
from django.db import models

# Create your models here.


class Photo(models.Model):
    image = models.ImageField(upload_to='users/photos/')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='gallery')


class FavouriteOrganization(models.Model):
    organization = models.ForeignKey('organizations.Organization', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class Test(models.Model):
    title = models.CharField(max_length=64)
    image = models.ImageField(upload_to='images/tests/')


class Bonus(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.IntegerField()
    descr = models.TextField()
