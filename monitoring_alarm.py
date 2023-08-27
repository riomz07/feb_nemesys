
import threading, time, django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','nemesys_feb.settings')
django.setup()

from main.models import NetworkDevice
from main.logic.NetMaps import NetMapsLogic
import requests



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
        all_device = NetworkDevice.objects.all()
        for device in all_device:
            check_device = NetMapsLogic(device.ip_address)
            if check_device.check_response == 'off':
                print(device.name+' = Offline')
                report_to_telegram(f"Assalamualaikum Admin, ada masalah : \n{device.name} Status Offline")
            else:
                print(device.name+' = Online')
        # Tunggu 1 menit sebelum memeriksa kembali
        time.sleep(5)

# Buat thread untuk menjalankan fungsi pengecekan
device_check_thread = threading.Thread(target=check_device_availability)

# Mulai thread
device_check_thread.start()
