from django.contrib import admin
from . import models

@admin.register(models.NetworkDevice)
class NetworkDeviceAdmin(admin.ModelAdmin):
    list_display = ['name', 'ip_address', 'last_status']


admin.site.site_header = 'FEB Nemesys Website Admin'