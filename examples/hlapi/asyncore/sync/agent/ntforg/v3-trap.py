"""
SNMPv3 TRAP: auth SHA, privacy: AES128
++++++++++++++++++++++++++++++++++++++

Send SNMP notification using the following options:

* SNMPv3
* with local snmpEngineId = 0x8000000001020304 (must configure at Receiver)
* with user 'usr-sha-aes128', auth: SHA, priv: AES128
* over IPv4/UDP
* send TRAP notification
* with TRAP ID 'authenticationFailure' specified as a MIB symbol
* do not include any additional managed object information

SNMPv3 TRAPs requires pre-sharing the Notification Originator's
value of SnmpEngineId with Notification Receiver. To facilitate that
we will use static (e.g. not autogenerated) version of snmpEngineId.

Functionally similar to:

| $ snmptrap -v3 -l authPriv -u usr-sha-aes -A authkey1 -X privkey1 \
|            -a SHA -x AES \
|            demo.snmplabs.com \
|            12345 \
|            1.3.6.1.4.1.20408.4.1.1.2 \
|            '1.3.6.1.2.1.1.1.0' s 'my system'

"""#
from pysnmp.hlapi import *

errorIndication, errorStatus, errorIndex, varBinds = next(
    sendNotification(SnmpEngine(OctetString(hexValue='8000000001020304')),
                     UsmUserData('usr-sha-aes128', 'authkey1', 'privkey1',
                                 authProtocol=usmHMACSHAAuthProtocol,
                                 privProtocol=usmAesCfb128Protocol),
                     UdpTransportTarget(('demo.snmplabs.com', 162)),
                     ContextData(),
                     'trap',
                     NotificationType(
                         ObjectIdentity('SNMPv2-MIB', 'authenticationFailure')
                     )
    )
)
if errorIndication:
    print(errorIndication)
