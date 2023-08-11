from django.urls import path
from main import views


urlpatterns = [
    path('login', views.login_user, name='login'),
    path('logout', views.logout_user, name='logout'),
    path('', views.main, name='main'),
    path('netmaps', views.netmaps, name='netmaps'),
    path('configure/', views.configure, name='configure'),
    path('add_network_devices', views.add_network_device, name='add_network_device'),
    path('edit_network_devices', views.edit_network_device, name='edit_network_device'),
    path('delete_network_device', views.delete_network_device, name='delete_network_device'),
    path('get_netmaps_data', views.netmaps_data, name='get_netmaps_data'),
]