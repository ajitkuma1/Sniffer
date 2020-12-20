import netmiko
import yaml
import getpass
import re
import os

class color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


with open('device.yaml', 'r') as handle:
    data = yaml.safe_load(handle)
    print(data['9800-WLC']['pass'])

def writeToFile(output):
    with open(f"/tmp/{9800}_facts.txt", "w") as handle:
        handle.write(output)




def test():

    net_connect = netmiko.ConnectHandler(host = data['9800-WLC']['ipAddress'],username = data['9800-WLC']['username'],password = 'bgl12', device_type= 'cisco_ios',)
    a = net_connect.check_enable_mode()

    net = netmiko.ConnectHandler()

    if net_connect.check_enable_mode() == True:
        print("Test Passed")
        input(color.PURPLE + "Enter Enable Password:" + color.END)


    print(a)

    net_connect.cleanup()
    return()

#test()

#print(net_connect.find_prompt())
#prompt = net_connect.find_prompt()
#concat_output = ""
#for c in data['9800-WLC']['commands']:
#    out = net_connect.send_command(c)
#    concat_output += '\n\n'+ prompt + c + '\n\n'
#    concat_output += '\n' + out
##    print(color.PURPLE + prompt + c + color.END)
#    print(out)
#
#writeToFile(concat_output)


clSumm = """Number of Clients: 1

MAC Address    AP Name                                        Type ID   State             Protocol Method     Role
-------------------------------------------------------------------------------------------------------------------------
503e.aadb.9248 APC4B9.CDF2.0D08                               WLAN 17   Run               11ac     Dot1x      Local

Number of Excluded Clients: 0"""

clientSummary = "(\w+.\w+.\w+)\s+(\w+.\w+.\w+)\s+(\w+\s+\d+)\s+(\w+)\s+(\w+)\s+(\w+).*"
b = re.search(clientSummary, clSumm)
print(b.group(1), b.group(2), b.group(3), b.group(4), b.group(5), b.group(6))


cntPlane = """

9800-WLC#show wireless fabric control-plane wncd 0
Control-plane:
Name                             IP-address        Key                              Status
--------------------------------------------------------------------------------------------
default-control-plane            30.0.1.10         15026e                           Up
default-control-plane            30.0.1.11         15026e                           Up
"""

cntPattern = "\w+\s+(\d+.\d+.\d+.\d+)\s+.*"

controllers = re.findall(cntPattern, cntPlane)

print(controllers[0], controllers[1])




clientDetails = """

9800-WLC#show wireless client mac-address 503e.aadb.9248 detail

Client MAC Address : 503e.aadb.9248
Client IPv4 Address : 192.168.10.12
Client IPv6 Addresses : fe80::b0ac:2fe8:4461:d4ae
                        2401:b00:11:83:b0ac:2fe8:4461:d4ae
                        2401:b00:11:83:4906:7ee8:1014:6084
Client Username : dnac
AP MAC Address : c4b9.cdf2.9460
AP Name: APC4B9.CDF2.0D08
AP slot : 1
Client State : Associated
Policy Profile : Escalation_Global_F_3c449ee3
Flex Profile : default-flex-profile
Wireless LAN Id: 17
WLAN Profile Name: Escalation_Global_F_3c449ee3
Wireless LAN Network Name (SSID): EscalationFabric1.3_Dot1x
BSSID : c4b9.cdf2.946e
Connected For : 10328 seconds
Protocol : 802.11ac
Channel : 108
Client IIF-ID : 0xa0000001
Association Id : 1
Authentication Algorithm : Open System
Re-Authentication Timeout : 18000 sec (Remaining time: 7673 sec)
Session Warning Time : Timer not running
Input Policy Name  : None
Input Policy State : None
Input Policy Source : None
Output Policy Name  : None
Output Policy State : None
Output Policy Source : None
WMM Support : Enabled
U-APSD Support : Enabled
  U-APSD value : 0
  APSD ACs    : BK, BE, VI, VO
Fastlane Support : Disabled
Client Active State : Active
Power Save : OFF
Current Rate : m9 ss1
Supported Rates : 18.0,36.0,48.0,54.0
Mobility:
  Move Count                  : 0
  Mobility Role               : Local
  Mobility Roam Type          : None
  Mobility Complete Timestamp : 05/17/2020 05:56:02 UTC
Client Join Time:
  Join Time Of Client : 05/17/2020 05:56:02 UTC
Policy Manager State: Run
Last Policy Manager State : IP Learn Complete
Client Entry Create Time : 10327 seconds
Policy Type : WPA2
Encryption Cipher : CCMP (AES)
Authentication Key Management : 802.1x
Encrypted Traffic Analytics : No
Protected Management Frame - 802.11w : No
EAP Type : PEAP
VLAN : default
Multicast VLAN : 0
WFD capable : No
Managed WFD capable : No
Cross Connection capable : No
Support Concurrent Operation : No
Session Manager:
  Point of Attachment : capwap_90000006
  IIF ID             : 0x90000006
  Authorized         : TRUE
  Session timeout    : 18000
  Common Session ID: 04060005000003C021341951
  Acct Session ID  : 0x00000000
  Last Tried Aaa Server Details:
  	Server IP : 5.0.6.3
  Auth Method Status List
  	Method : Dot1x
  		SM State         : AUTHENTICATED
  		SM Bend State    : IDLE
  Local Policies:
  	Service Template : wlan_svc_Escalation_Global_F_3c449ee3 (priority 254)
  		VLAN             : 1
  		Absolute-Timer   : 18000
  Server Policies:
  Resultant Policies:
  		VLAN Name         : default
  		VLAN             : 1
  		Absolute-Timer   : 18000
DNS Snooped IPv4 Addresses : None
DNS Snooped IPv6 Addresses : None
Client Capabilities
  CF Pollable : Not implemented
  CF Poll Request : Not implemented
  Short Preamble : Not implemented
  PBCC : Not implemented
  Channel Agility : Not implemented
  Listen Interval : 0
Fast BSS Transition Details :
  Reassociation Timeout : 0
11v BSS Transition : Not implemented
11v DMS Capable : No
QoS Map Capable : No
FlexConnect Data Switching : N/A
FlexConnect Dhcp Status : N/A
FlexConnect Authentication : N/A
FlexConnect Central Association : N/A
Client Statistics:
  Number of Bytes Received : 117275
  Number of Bytes Sent : 288327
  Number of Packets Received : 866
  Number of Packets Sent : 4415
  Number of Policy Errors : 0
  Radio Signal Strength Indicator : -27 dBm
  Signal to Noise Ratio : 58 dB
Fabric status : Enabled
  RLOC    : 30.0.1.25
  VNID    : 8188
  SGT     : 0
  Control plane name  : default-control-plane
Client Scan Reports
Assisted Roaming Neighbor List
Nearby AP Statistics:
EoGRE : No/Simple client
Device Type      : Microsoft-Workstation
Device Name      : MSFT 5.0
Protocol Map     : 0x000009  (OUI, DHCP)
Protocol         : DHCP
Type             : 12   19
Data             : 13
00000000  00 0c 00 0f 44 45 53 4b  54 4f 50 2d 30 55 48 4c  |....DESKTOP-0UHL|
00000010  47 48 50                                          |GHP             |
Type             : 60   12
Data             : 0c
00000000  00 3c 00 08 4d 53 46 54  20 35 2e 30               |.<..MSFT 5.0    |
Type             : 55   17
Data             : 11
00000000  00 37 00 0d 01 03 06 0f  1f 21 2b 2c 2e 2f 79 f9  |.7.......!+,./y.|
00000010  fc                                                |.               |


"""

clientPattern = "(Client+\s+.*)"
ApPattern = "(AP+\s+.*)"

clientName = re.findall(clientPattern, clientDetails)
ApInfo = re.findall(ApPattern, clientDetails)
re.su

print(color.GREEN + clientName[1], clientName[2] + color.END)
print(clientName)
print (ApInfo)

#for l in a.split('\n'):
#    print(l)
#    if l:
#        b = re.search(pattern,l)
#        if b.group() == None:
#            print(l)
#    else:
#        print('Nothing')

#b = re.findall(pattern,a)
#print(b)

str = 'an example word:cat!!'
match = re.search(r'word:\w\w\w', str)
# If-statement after search() tests if it succeeded
if match:
  print (match.group()) ## 'found word:cat'
else:
  print('did not find')


a = "show ip int brief"
if type(a) is 'str':
    print(Ajitesh)

print(type(ApInfo))


# Python3 code to demonstrate
# Check if variable is string
# using isinstance()

# initializing string
test_string = "GFG"
print(type(test_string))

#res = type(test_string)
#res = isinstance(test_string, str)
#print("Is variable a string ? : " + str(res))

if isinstance(test_string, (list, tuple)):
    print('Ajitesh')

filename = "/tmp/abcd.txt"

if os.path.