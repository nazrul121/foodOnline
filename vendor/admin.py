from django.contrib import admin
from .models import Vendor

class VendorAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('vendor_name',)}
    list_display = ['user', 'user_phone_number', 'vendor_name', 'is_approved', 'created_at']
    list_display_links = ['user', 'vendor_name']
    list_editable = ['is_approved']

    def user_phone_number(self, obj):
        return obj.user.phone_number

    user_phone_number.short_description = 'Phone Number'

# Register your models here.
admin.site.register(Vendor, VendorAdmin)
