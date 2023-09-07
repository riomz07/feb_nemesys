from django.db import models


class NetworkDevice(models.Model):
    
    CHOICES = (
        ('Router','Router'),
        ('Switch Manage','Switch Manage'),
        ('Switch UnManage','Switch UnManage'),
        ('AP','AP')
    )

    name = models.CharField(max_length=100,null=True)
    lat = models.FloatField(null=True)
    long = models.FloatField(null=True)
    ip_address = models.GenericIPAddressField(max_length=100, null=True)
    last_status = models.BooleanField(null=True, blank=True, default=False)
    daily_restart_status = models.BooleanField(null=True, blank=True, default=False)
    fail_check = models.IntegerField(null=True, blank=True, default=0)
    latency = models.IntegerField(null=True, blank=True, default=0)
    type = models.CharField(max_length=100,null=True, choices=CHOICES)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Network Device'
        verbose_name_plural = 'Network Devices'
        ordering = ['name']

class SummaryRestart(models.Model):
    
    summary = models.CharField(max_length=300,null=True, blank=True)
    time = models.DateTimeField(auto_now_add=True)


    def __str__(self) -> str:
        return self.summary

    class Meta:
        verbose_name = 'Summary Restart'
        verbose_name_plural = 'Summaries Restart'
        ordering = ['summary']


class RestartStatus(models.Model):
    
    status = models.BooleanField(null=True, blank=True, default=False)


    def __str__(self) -> str:
        return self.status

    class Meta:
        verbose_name = 'Status Restart'
        verbose_name_plural = 'Status Restart'
        ordering = ['status']