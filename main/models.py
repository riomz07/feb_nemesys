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
    latency = models.IntegerField(null=True, blank=True, default=0)
    type = models.CharField(max_length=100,null=True, choices=CHOICES)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = 'Network Device'
        verbose_name_plural = 'Network Devices'
        ordering = ['name']
