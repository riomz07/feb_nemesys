from django import forms
from . import models

class NetworkDeviceForm(forms.ModelForm):
    
    CHOICES = (
        ('AP','AP'),
        ('Switch Manage','Switch Manage'),
        ('Switch UnManage','Switch UnManage'),
        ('Router','Router'),
    )

    name = forms.CharField( widget= forms.TextInput(attrs={'class':'form-control'}))
    lat = forms.FloatField(widget= forms.NumberInput(attrs={'class':'form-control'}))
    long = forms.FloatField(widget= forms.NumberInput(attrs={'class':'form-control'}))
    ip_address = forms.GenericIPAddressField(widget=forms.TextInput(attrs={'class':'form-control'}))
    type = forms.ChoiceField(choices=CHOICES , widget= forms.Select(attrs={'class':'form-select'}))

    class Meta:
        model = models.NetworkDevice
        fields = ['name','lat','long','ip_address','type']