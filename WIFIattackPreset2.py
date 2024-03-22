"""
@Author: n1sec
"""
#/usr/bin/python3

import sys, signal, argparse, subprocess
from colorama import Fore, Style

def handler(sig, frame):
    print(Fore.RED + "\n[!] Process interrupted...\n" + Style.RESET_ALL)
    sys.exit(1)

def disable_process():
    print(Fore.GREEN + "\n[!] Disable network processes....")
    subprocess.call(["sudo", "service", "NetworkManager", "stop", "&&", "sudo", "service", "wpa_supplicant", "stop"])
    print("[*] Process disabled successfully\n" + Style.RESET_ALL)
    
def restore():
    print(Fore.YELLOW + "\n[!] Restoring default network settings....")
    subprocess.call(["sudo", "service", "NetworkManager", "restart", "&&", "sudo", "service", "wpa_supplicant", "restart"])
    print("[*] Configuration successfully restored....\n" + Style.RESET_ALL)

def list_network_interfaces():
    print(Fore.GREEN + "\n[*] Network interfaces...")
    print("-" * 33 + Style.RESET_ALL)
    subprocess.call(["iwconfig"])

def monitor_mode(interface):
    print(Fore.GREEN + "\n[!] Switch to monitor mode....")
    subprocess.call(["sudo", "ifconfig", interface, "down"])
    subprocess.call(["sudo", "iwconfig", interface, "mode", "Monitor"])
    subprocess.call(["sudo", "ifconfig", interface, "up"])
    print("[*] Successful process" + Style.RESET_ALL)
    
def main():
    signal.signal(signal.SIGINT, handler)
    parser = argparse.ArgumentParser(description="Host preconfiguration for network attacks.")
    parser.add_argument("-l", "--list", action="store_true", help="Displays the network interfaces that the host has.")
    parser.add_argument("-d", "--disable", action="store_true", help="Disables network processes in the background")
    parser.add_argument("-i", "--interface", nargs="?", help="Specify the network interface, to switch to monitor mode.")
    parser.add_argument("-r", "--restore", action="store_true", help="Restore background network processes and altered network interface.")
    args = parser.parse_args()
    
    if args.disable:
        disable_process()
        
    elif args.restore:
        restore()
    
    elif args.list:
        list_network_interfaces()
    
    elif args.interface:
        monitor_mode(args.interface)
    
    else:
        parser.print_help()
        sys.exit()

if __name__ == "__main__":
    main()