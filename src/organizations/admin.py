from django.contrib import admin

from .models import Category, Location, Organization, OrganizationImage, Region

# Register your models here.


models = [Category, Location, OrganizationImage, Region]

for model in models:
    admin.site.register(model)


class OrganizationImageInline(admin.TabularInline):
    model = OrganizationImage
    readonly_fields = ['id']
    extra = 1


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'phone', 'website']
    inlines = [OrganizationImage]
