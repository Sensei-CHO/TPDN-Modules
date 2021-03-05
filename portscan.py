import sys
from pathlib import Path
import os
import cmd


from src import tpdnlib
from src import libinstaller

try:
    import nmap
    
except ModuleNotFoundError:
    libinstaller.install_packages("python-nmap")

finally:
    import nmap
    
def scanport(arg):
    ip, ports = arg.split(" ", 1)
    try:
        nm = nmap.PortScanner()
    except nmap.nmap.PortScannerError:
        print(tpdnlib.Color("red")("You need to install nmap first!"))
        exit()
        
    nm.scan(ip, ports)
    
    for host in nm.all_hosts():
        print(tpdnlib.Color("yellow")("----------------------------------------------------"))
        print(tpdnlib.Color("yellow")("Host:"), tpdnlib.Color("cyan")(host), tpdnlib.Color("cyan")(nm[host].hostname()))
        if nm[host].state() == "up":
            statecolor = "green"
        else:
            statecolor = "red"

        print(tpdnlib.Color("yellow")("State:"), tpdnlib.Color(statecolor)(nm[host].state()))

        for proto in nm[host].all_protocols():
            print(tpdnlib.Color("yellow")("--------------"))
            print(tpdnlib.Color("yellow")("Protocol:"), tpdnlib.Color("cyan")(proto))
            lport = nm[host][proto].keys()
            sorted(lport)
            for port in lport:

                if nm[host][proto][port]['state'] == "open":
                    statecolor = "green"
                else:
                    statecolor = "red"
                
                print(tpdnlib.Color("yellow")("port:"), tpdnlib.Color("cyan")(port), tpdnlib.Color(statecolor)(nm[host][proto][port]['state']))

        print(tpdnlib.Color("yellow")("----------------------------------------------------"))

class PromptShell(cmd.Cmd):
    intro = tpdnlib.Color("cyan")("Type help or ? to list commands.\n")
    prompt = tpdnlib.Color("yellow")("port scanner>")

    def __init__(self):
        super(PromptShell, self).__init__()

    def do_back(self, arg):
        "Exit the module and return to TPDN: back"

        return True
    
    def do_clear(self, arg):
        "Clear the terminal: clear"

        print(tpdnlib.Color("cyan")("Exiting module..."))
        tpdnlib.clear()

    def do_scanport(self, arg):
        "scan a port: portscan <ip> <ports or port range>"
        try:
            scanport(arg)
        except ValueError:
            print(tpdnlib.Color("red")("Oops! You may have forgotten to specify a parameter in your command!"))
def start():

    tpdnlib.figlet("port scanner", "magenta")
    try:
        shell = PromptShell()
        shell.cmdloop()

    except KeyboardInterrupt:
        print(tpdnlib.Color("cyan")("Exiting module..."))
        tpdnlib.clear()
