#!/usr/bin/python3.12
from argparse import ArgumentParser
from re import search
from subprocess import call, check_output


def get_args():
    """Arguments from user."""
    parser = ArgumentParser()
    parser.add_argument("-i", "--interface", help="An interface.")
    parser.add_argument("-n", "--newmac", help="An interface.")
    args = parser.parse_args()
    if not args.interface:
        parser.error("\n[-] Specify an interface. EX: eth0, en0, wlan0.")
    elif not args.newmac:
        parser.error("\n[-] Specify your NEW MAC!")
    return args


def get_current_mac(interface):
    """Get and output our current MAC address."""
    ifconfig_result = check_output(["ifconfig", interface], text=True)
    extract_mac_res = search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    if extract_mac_res:
        return extract_mac_res.group(0)
    else:
        print("\n[-] Couldn't read MAC!")


def get_new_mac(interface, new_mac):
    """Change current MAC to new MAC address."""
    current_mac = get_current_mac(interface)
    print(f"\n[!] Using interface: {interface}"
          f"\n[!] Current MAC: {current_mac}"
          f"\n\n\t[+] Your NEW MAC address: {new_mac}"
          f"\n-----------------------------------------------")
    call(["ifconfig", interface, "down"])
    call(["ifconfig", interface, "hw", "ether", new_mac])
    call(["ifconfig", interface, "up"])


user_args = get_args()
get_new_mac(user_args.interface, user_args.newmac)
