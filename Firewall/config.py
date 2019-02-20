#!/usr/bin/python3
## FIREWALL CONFIG FILE

# Home Directory
HOMEDIR="/home/free/Desktop/TOOLS/Firewall"

#Outside Interface
WANIFACE="eth0"

#Inside Interface
INIFACE="eth0"

#Inside IP Address
INIPADDR=''

#Local network
LOCALNET="192.168.5.0/24"

#Block External DNS Queries
EXTERNALDNS=True

#URL CATEGORIES
MALICIOUS=1
VPN=0
ADULT=0
DRUGS=0
GUNS=0
DYNDNS=0
ADS=0
SOCIALMEDIA=0
TEENTOP50=1

# WHITE LISTED MACS
MACS={'aa:aa:aa:aa:aa:aa', 'bb:bb:bb:bb:bb:bb', 'd0:77:14:99:ac:f3'}
