from django.contrib import admin
from vendor.models import Vendor
# Register your models here.

class VendorAdmin(admin.ModelAdmin):
    list_display = ['user', 'Vendor_name', 'is_approved', 'created_at',]
    list_display_links=['user', 'Vendor_name',]




admin.site.register(Vendor,VendorAdmin)
