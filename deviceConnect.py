import netmiko
import yaml
import re
import time
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

class deviceConnect():
    def __init__(self):
        self.fileCheck = 0  #check whether log file exists.

    def writeToFile(self, devicehostname, output):

        print("check global variable", self.fileCheck)

        """Open a new file for log collection,
           Append if the file already exists
        """
        if self.fileCheck == 0 :
            filename = "/tmp/" + devicehostname + time.strftime("%d-%m-%Y-%H%M%S")+"_logs.txt"
            self._fName = filename
            self.fileCheck =+ 1

        if self.fileCheck == 1:
            with open(self._fName, "a") as handle:
                handle.write(output)
                handle.close()
        else:
            #filename = "/tmp/" + deviceHostname + "_logs.txt"
            #self._filename = filename
            with open(self._fName, "w") as handle:
                handle.write(output)
                handle.close()



    def sendCommand(self,connectParam, cmd):
        try:
            net_connect = netmiko.ConnectHandler(**connectParam)
        except TimeoutError as timeErr:
            print("Openation timed out, check connectivity.")
            print(timeErr)
            return
        except:
            print("Authentication failed! Please check username and Password and device connectivity.")
            return
        if net_connect.check_enable_mode() !=True:
            input(color.PURPLE + "Enter Enable Password:" + color.END)
        prompt = net_connect.find_prompt()
        deviceHostName = prompt.strip('#')

        #filename = "/tmp/" + deviceHostname + time.strftime("%d-%m-%Y-%H%M%S") + "_logs.txt"
        concat_output = ""

        if isinstance(cmd, (list,tuple)):
            for c in cmd:
                out = net_connect.send_command(c)
                concat_output += '\n\n' + prompt + c
                concat_output += '\n' + out
                print(color.PURPLE + prompt + c + color.END)
                print(out)
        else:
            out = net_connect.send_command(cmd)
            concat_output += '\n\n' + prompt + cmd
            concat_output += '\n' + out
            print(color.PURPLE + prompt + cmd + color.END)
            print(out)
        deviceConnect.writeToFile(self, deviceHostName, concat_output)

    def wirelessClientStatus(self, connectionP, command):
        #self.macAddress = macAddress
        self.connectP = connectionP
        self.cmd = command
        print("Summary of wireless client")
        deviceConnect.sendCommand(self,connectionP,command)


def main():
    with open('device.yaml', 'r') as handle:
        data = yaml.safe_load(handle)
        print(data['9800-WLC']['pass'])
        a= data['9800-WLC']['wirelessClient']
        print(len(a))

    wlc9800 = {
        'host': data['9800-WLC']['ipAddress'],
        'username': input(color.PURPLE + "Enter wireless controller username:" + color.END),
        'password': input(color.PURPLE + "Enter wireless controller password:" + color.END),
        'device_type' : 'cisco_ios',
        'session_timeout' : 60,
        'timeout': 5
    }


    cmd = data['9800-WLC']['commands']
    clientcmd = data['9800-WLC']['wirelessClient']
    print(clientcmd)
    wlc = deviceConnect()
    wlc.sendCommand(wlc9800, "show ip int brief")
    wlc.sendCommand(wlc9800, "show ap summary")

    wlc.sendCommand(wlc9800, "show wireless client summary")
    wlc.sendCommand(wlc9800,clientcmd)


    #wlc.wirelessClientStatus(wlc9800, clientcmd)


if __name__ == "__main__":
    main()




