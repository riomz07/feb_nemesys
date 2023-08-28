
import threading, time, django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','nemesys_feb.settings')
django.setup()

from main.models import NetworkDevice
from main.logic.NetMaps import NetMapsLogic
import requests
import datetime



#Report to telegram
def report_to_telegram(message):    
    apiToken = '6534614709:AAHgbcGnLgAXhE4lgkhz9E5-bMluFboi6ww'
    chatID = '-931159956'
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'
    try:
        response = requests.post(apiURL, json={'chat_id': chatID, 'text': message})
        print("Send Notification to Telegram")
    except Exception as e:
        print(e)


def check_device_availability():
    while True:
        # Lakukan logika pengecekan ketersediaan perangkat di sini
        print("Mengecek availability perangkat...")
        try:
            all_device = NetworkDevice.objects.all()
            for device in all_device:
                check_device = NetMapsLogic(device.ip_address)
                current_status = check_device.check_response()                            
                # if last status on & device status now off :
                # 	change status to off
                # 	and notif detil with time 
                if current_status == 'off' and device.last_status == True:
                    device.last_status = False
                    device.save()
                    print(device.name+ ' = Offline')
                    now = datetime.datetime.now()
                    formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
                    report_to_telegram(f"Astagfirullah we have some problem : \n{device.name} \nStatus : Offline\nTime : {formatted_time}") 
                # if last status off & device status now on:
                # 	change status to on
                # 	and notif detil with time 
                elif current_status == 'on' and device.last_status == False:
                    device.last_status = True
                    device.save()
                    print(device.name+ ' = Back Online')
                    now = datetime.datetime.now()
                    formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
                    report_to_telegram(f"Alhamdulillah problem have been solve : \n{device.name} \nStatus : Online\nTime : {formatted_time}")
                else:
                    print(device.name+' = Online')
            # Tunggu 1 menit sebelum memeriksa kembali
            time.sleep(60)
        except Exception as error:
            print ('Error : '+ error)

# Buat thread untuk menjalankan fungsi pengecekan
device_check_thread = threading.Thread(target=check_device_availability)

# Mulai thread
device_check_thread.start()
