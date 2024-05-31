import threading, time, django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','nemesys_feb.settings')
django.setup()

from main.models import NetworkDevice, SummaryRestart, RestartStatus
from main.logic.NetMaps import NetMapsLogic
import requests
import datetime
import paramiko



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

#variable user dan password ssh
user = "aproot"
passw = "Asdf123#"

#variable kalkulasi summary 
total_ap = 0
ap_berhasil = 0
ap_gagal = 0
list_ap_gagal = set()

#inisiasi variable paramiko
ssh = paramiko.SSHClient()


#membuat fungsi ssh dengan 5 parameter 
def run_command_on_device(ip_address, username, password, command, device_name):
        # Load SSH host keys.
        ssh.load_system_host_keys()
        # Add SSH host key automatically if needed.
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        for attemp in range(1,4):
            #try jika berhasil
            try:
                print("Percobaan Koneksi ke : %s" %attemp)
                #Mengkoneksikan ssh ke ip menggunakan user dan pass yang telah di deklarasikan
                ssh.connect(ip_address, username=username,password=password,look_for_keys=False)
                #eksekusi perintah
                ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command)
                #insiasi output ke variable (gk perlu)
                output = ssh_stdout.readlines()
                #tutup koneksi
                ssh.close()
                
                print(f"Berhasil Reboot {device_name} #  {str(attemp)}")

                #inisiasi global variable
                global ap_berhasil
                #tambah value
                ap_berhasil += 1

                return output

            #jika gagal
            except Exception as error_message:

                print(f"Tidak dapat terkoneksi {device_name} #  {str(attemp)}")
                
                #inisiasi global variable   
                global ap_gagal
                global list_ap_gagal

                print(device_name in list_ap_gagal)
                
                #jika nama perangkat belum terdaftar tambah ke list daftar ap gagal
                if device_name not in list_ap_gagal:
                    ap_gagal +=1

                #tambahkan ke daftar ap gagal    
                list_ap_gagal.add(f"{device_name}")


def check_device_availability():
    while True:
        all_device = NetworkDevice.objects.all()
        try:
            #------------------
            #Handle Check Availability Perangkat
            #------------------
            # check Device availability dengan minium 3x fail check baru rubah status 
            print("Mengecek availability perangkat...")
            for device in all_device:
                check_device = NetMapsLogic(device.ip_address)
                current_status = check_device.check_response()            


                #Jika current status off and last on too
                if current_status == 'off' and device.last_status == True:
                    #Jika perangkat sudah terhitung 3 menit mati... jadikan last status menjadi False/Offline
                    if device.fail_check == 3 :
                        device.last_status = False
                        device.fail_check += 1
                        device.save()

                        #Notif
                        print(device.name + ' = Offline')
                        now = datetime.datetime.now()
                        formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
                        report_to_telegram(f"🚨🚨🚨🚨🚨\nAstagfirullah we have some problem : \n{device.name} \nStatus : Offline\nTime : {formatted_time}") 

                    elif device.fail_check == 1440:
                        device.fail_check += 1
                        device.save()

                        #Notif
                        print(device.name + ' = Offline 1 Day')
                        now = datetime.datetime.now()
                        formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
                        report_to_telegram(f"🚨🚨🚨🚨🚨\nAstagfirullah Device Already 1 Day Offline : \n{device.name} \nStatus : 1 Day Offline\nTime : {formatted_time}") 

                    else:
                        device.fail_check += 1
                        device.save()

                #If Current Status Offline and Last Status Offline too
                elif current_status == 'off' and device.last_status == False:
                    print(device.name + ' Already Offline Add 1 fail check')
                    device.fail_check += 1
                    device.save()


                elif current_status == 'on' and device.last_status == True:
                    device.last_status = True
                    device.fail_check = 0
                    device.save()
                    print(device.name + ' Stay Online')

                elif current_status == 'on' and device.last_status == False:
                    device.last_status = True
                    device.fail_check = 0
                    device.save()

                    print(device.name+ ' = Back Online')
                    now = datetime.datetime.now()
                    formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
                    report_to_telegram(f"✅✅✅✅✅\nAlhamdulillah problem have been solve : \n{device.name} \nStatus : Online\nTime : {formatted_time}")

                else:
                    device.last_status = True
                    device.fail_check = 0
                    device.save()


            # Dapatkan waktu saat ini
            waktu_sekarang = datetime.datetime.now().time()
            # Tentukan rentang waktu yang ingin Anda periksa
            rentang_waktu_mulai = datetime.time(0, 0)  # Jam 00:00
            rentang_waktu_selesai = datetime.time(0, 59)  # Jam 00:59
            rentang_waktu_reset = datetime.time(1, 0)  # Jam 1:00
            rentang_waktu_reset = datetime.time(1, 59)  # Jam 1:59

            restart_status = RestartStatus.objects.latest('status')

            # Waktu Restart
            if rentang_waktu_mulai <= waktu_sekarang <= rentang_waktu_selesai and restart_status.status == False:

                global total_ap
                global ap_berhasil
                global ap_gagal
                global list_ap_gagal

                print('Masuk waktu reboot')
                for device in all_device:
                    run_command_on_device(device.ip_address, user, passw, "reboot", device.name)

                report_to_telegram(f"Summary Midnight Reboot AP FEB\nTime: {waktu_sekarang}\nTotal AP: {total_ap}\nBerhasil Reboot : {ap_berhasil}\nGagal Reboot : {ap_gagal}\nList AP yang gagal reboot : \n{list_ap_gagal}")

                summary_restart = SummaryRestart(summary = f"Summary Midnight Reboot AP FEB, Time: {waktu_sekarang}, Total AP: {total_ap}, Berhasil Reboot : {ap_berhasil}, Gagal Reboot : {ap_gagal}, List AP yang gagal reboot : , {list_ap_gagal}" )
                summary_restart.save()
                
                # Reset all count
                total_ap = 0
                ap_berhasil = 0
                ap_gagal = 0
                list_ap_gagal = set()

                restart_status.status = True
                restart_status.save()
                
            # Waktu Reset 
            elif rentang_waktu_reset <= waktu_sekarang <= rentang_waktu_reset and restart_status == True:
                restart_status.status = False
                restart_status.save()
                print('Reset -has been reboot- ')
            else:
                pass


            # Tunggu 1 menit sebelum memeriksa kembali
            time.sleep(60)

        except Exception as error:
            print ('Error : '+ error)

# Buat thread untuk menjalankan fungsi pengecekan
device_check_thread = threading.Thread(target=check_device_availability)

# Mulai thread
device_check_thread.start()
