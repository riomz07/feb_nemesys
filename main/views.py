from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .logic.NetMaps import NetMapsLogic
from .decorators import unauth_user
from . import models, form
import subprocess

####
# Handle Login
####
@unauth_user
def login_user(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('main')
        else:
            messages.error(request, 'Username or Password Incorrect')
    else:
        pass

    return render(request, 'login.html')

####
# Handle Logout
####
@login_required(login_url='login')
def logout_user(request):
    logout(request)
    return redirect('login')


####
# Handle Main Page
####
@login_required(login_url='login')
def main(request):

    all_device = models.NetworkDevice.objects.all()
    total_device = all_device.count()

    ##Count Total
    total_online = 0
    total_offline = 0
    best_device_latency = None
    worst_device_latency = None
    best_latency = float('inf')
    worst_latency = 0
    devices_online = []
    devices_offline = []

    for device in all_device:
        device_ip = device.ip_address
        device_logic = NetMapsLogic(device_ip)
        if device_logic.check_response() == "on":
            
            total_online += 1
            devices_online.append(device)

            result_latencty = float(device_logic.check_latency())
            print(result_latencty)
            if result_latencty is not None:
                print(result_latencty)
                
                ## Jadi cek apakah result lebih kecil dari pada infinity
                if result_latencty < best_latency :
                    print('masuk best')
                    best_device_latency = device.name
                    best_latency = result_latencty  
                ## Jadi cek apakah result lebih best dari pada 0
                if result_latencty > worst_latency :
                    print('masuk worst')
                    worst_device_latency = device.name
                    worst_latency = result_latencty

        else:
            total_offline +=1
            devices_offline.append(device)
        
            

    context = {
        'total_device':total_device,
        'total_online':total_online,
        'total_offline':total_offline,
        'best_latency': f"{best_device_latency} ({round(best_latency, 2)})",
        'worst_latency': f"{worst_device_latency} ({round(worst_latency, 2)})",
        'all_devices': all_device,
        'devices_online': devices_online,
        'devices_offline': devices_offline,
    }

    return render(request, 'dashboard.html',context)


####
# Handle Netmaps Page
####
@login_required(login_url='login')
def netmaps(request):
    return render(request, 'netmaps.html')


####
# Handle Configure Page
####
@login_required(login_url='login')
def configure(request):

    global device_id
    all_network_device = models.NetworkDevice.objects.all()

    if request.GET.get('device_id','none') != 'none':
        device_id = request.GET.get('device_id')
        device = models.NetworkDevice.objects.get(id=device_id)
        form_network_device = form.NetworkDeviceForm(instance=device)
    else:
        form_network_device = form.NetworkDeviceForm()
        device_id = None

    return render(request, 'configure.html',{'form_network_device':form_network_device, 'all_network_device':all_network_device,'device_id':device_id})


####
# Add Network Device Function
####

@login_required(login_url='login')
def add_network_device(request):

    form_network_device = form.NetworkDeviceForm(request.POST)

    if form_network_device.is_valid():
        form_network_device.save()
        messages.success(request, 'Sukses Tambah Network Device')
        return redirect('configure')
    else:
        messages.error(request,'Gagal Tambah Network Device periksa kembali inputan')
        return redirect('configure')
    


####
# Handle Edit Network Device Funciton
####
@login_required(login_url='login')
def edit_network_device(request):

    network_device = models.NetworkDevice.objects.get(id=request.POST.get('device_id'))
    form_network_device = form.NetworkDeviceForm(request.POST,instance=network_device)

    if form_network_device.is_valid():
        form_network_device.save()
        messages.success(request, 'Sukses Edit Network Device')
        return redirect('configure')
    else:
        messages.error(request,'Gagal Edit Network Device periksa kembali inputan')
        return redirect('configure')
    
@login_required(login_url='login')
def delete_network_device(request):

    if request.GET.get('device_id','none') != 'none':
        device_id = request.GET.get('device_id')
        device = models.NetworkDevice.objects.get(id=device_id)
        device.delete()
        messages.success(request,'Berhasil Delete Device')
        return redirect('configure')
    else:
        messages.error(request,'Gagal Delete Device')
        return redirect('configure')

@login_required(login_url='login')
def netmaps_data(request):
    list_device = models.NetworkDevice.objects.all()
    json_device=[]
    for device in list_device:
        device_name = device.name
        device_ip = device.ip_address

        netmaps_logic = NetMapsLogic(device_ip)
        device_status = netmaps_logic.check_response()
        device_latency = netmaps_logic.check_latency()
        icon = f"{device.type}_{device_status}"
        print(icon)
        
        json_device.append({
            'device_name':device_name,
            'lat':device.lat,
            'long':device.long,
            'type':device.type,
            'device_status':device_status,
            'device_latency':device_latency,
            'icon':icon
        })
        
    return JsonResponse({'devices':json_device})  


####
# Handle Services
####
@login_required(login_url='login')
def services(request):
    # Eksekusi perintah
    try:
        result_mes = subprocess.run(["systemctl status monitor", ""], stdout=subprocess.PIPE, text=True)
    except Exception as e:
        result_mes = e
    
    monitoring_engine_status = result_mes
    # Cetak hasil
    context = {'monitoring_engine_status':monitoring_engine_status}
    return render(request, 'services.html',context)



