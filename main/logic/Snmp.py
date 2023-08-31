from pysnmp.hlapi import *

# Konfigurasi target SNMP (ganti dengan alamat IP dan komunitas SNMP Anda)
target_ip = '10.1.1.40'
community_string = 'Jaringan'

# Definisikan OID yang ingin Anda ambil
oid_system_description = ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0)
oid_system_uptime = ObjectIdentity('SNMPv2-MIB', 'sysUpTime', 0)
oid_interface_description = ObjectIdentity('IF-MIB', 'ifDescr')
oid_interface_traffic_in = ObjectIdentity('IF-MIB', 'ifInOctets')
oid_interface_traffic_out = ObjectIdentity('IF-MIB', 'ifOutOctets')

# Buat sesi SNMP
snmp_session = SnmpEngine()

# Buat komunitas SNMP
community_data = CommunityData(community_string)

# Buat target SNMP
udp_transport_target = UdpTransportTarget((target_ip, 161))

# Membuat getCmd() untuk masing-masing OID yang ingin Anda ambil
system_description_command = getCmd(snmp_session, community_data, udp_transport_target, ContextData(), ObjectType(ObjectIdentity('.1.3.6.1.2.1.1.5.0')))
system_uptime_command = getCmd(snmp_session, community_data, udp_transport_target, ContextData(), oid_system_uptime)
interface_description_command = nextCmd(snmp_session, community_data, udp_transport_target, ContextData(), oid_interface_description)
interface_traffic_in_command = nextCmd(snmp_session, community_data, udp_transport_target, ContextData(), oid_interface_traffic_in)
interface_traffic_out_command = nextCmd(snmp_session, community_data, udp_transport_target, ContextData(), oid_interface_traffic_out)

# Eksekusi perintah getCmd() dan nextCmd()
error_indication, error_status, error_index, var_binds = next(system_description_command)
if error_indication:
    print(f"Error: {error_indication}")

error_indication, error_status, error_index, var_binds = next(system_uptime_command)
if error_indication:
    print(f"Error: {error_indication}")

for error_indication, error_status, error_index, var_binds in interface_description_command:
    if error_indication:
        print(f"Error: {error_indication}")
    else:
        for var_bind in var_binds:
            print(f"Interface Description: {var_bind[1].prettyPrint()}")

for error_indication, error_status, error_index, var_binds in interface_traffic_in_command:
    if error_indication:
        print(f"Error: {error_indication}")
    else:
        for var_bind in var_binds:
            print(f"Interface Traffic In: {var_bind[1].prettyPrint()}")

for error_indication, error_status, error_index, var_binds in interface_traffic_out_command:
    if error_indication:
        print(f"Error: {error_indication}")
    else:
        for var_bind in var_binds:
            print(f"Interface Traffic Out: {var_bind[1].prettyPrint()}")

# Tutup sesi SNMP
snmp_session.close()
