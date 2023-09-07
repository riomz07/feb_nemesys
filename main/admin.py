from django.contrib import admin
from . import models

@admin.register(models.NetworkDevice)
class NetworkDeviceAdmin(admin.ModelAdmin):
    list_display = ['name', 'ip_address', 'last_status','fail_check']

@admin.register(models.SummaryRestart)
class SummaryRestartAdmin(admin.ModelAdmin):
    list_display = ['summary','time']

@admin.register(models.RestartStatus)
class SummaryRestartAdmin(admin.ModelAdmin):
    list_display = ['status']


admin.site.site_header = 'FEB Nemesys Website Admin'