from django.contrib import admin
from . import models

@admin.register(models.NetworkDevice)
class NetworkDeviceAdmin(admin.ModelAdmin):
    list_display = ['name', 'ip_address', 'status']


admin.site.site_header = 'FEB Nemesys Website Admin'