from django.contrib import admin
from django.contrib.auth.models import Group
from . import models

admin.site.unregister(Group)


@admin.register(models.Discount)
class DiscountAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Contributor)
class ContributorAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Manufacture)
class ManufactureAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(models.DiscountSet)
class DiscountSetAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    pass
