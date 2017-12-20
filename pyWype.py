#!/usr/bin/env python
# TODO: add support for SD cards
# TODO: add classes for code resue

from __future__ import print_function
from builtins import input

# Python 2.7 & 3.4 disk wiping utility for use on Linux operating systems. RUN AS ROOT.
import sys              # For interpreter variables & associated functions
import os               # For operating system dependent functions
import re               # For regular expression parsing

# Define functions

def osCheck():
    """Check if OS is 'POSIX'"""

    if 'posix' not in os.name:
        print("This program was designed for Linux. Exiting.")
        sys.exit()

def userCheck():
    """Check is user has UID 0"""

    if not os.getuid() == 0:
	print("This program requires ROOT privileges. Exiting.")
	sys.exit()

def listDevices():
    """List mounted device(s) / partition(s)"""

    print(22 * "-", "DEVICES & PARTITIONS", 22 * "-")                                      # Header

    return os.system('lsblk /dev/sd* /dev/mmcblk* --nodeps --output NAME,MODEL,VENDOR,SIZE,TYPE,STATE')
    # lsblk -d -o NAME,MODEL,VENDOR...

def defineDevice():
    """Prompt user to define device or partition to wipe"""

    while True:
        try:
            device = str(input("Enter letter [and number] of device/partition to wipe,\ne.g. to wipe '/dev/sdb' enter 'b': "))

            if not re.match("^[a-z][0-9]?$", device):
                raise ValueError()
            return device

        except ValueError:
            print("Sorry, that's not a valid device or partition. Try again.")

def appendDevice():
    """Append user-defined device/partition to /dev/sd"""

    letter = defineDevice()

    return '/dev/sd' + letter

def numberOfWipes():
    """Prompt user for number of wipes to perform"""

    while True:
        try:
            wipes = int(input("How many times do you want to wipe the device or partition?: "))

            if not wipes > 0:
                raise ValueError()
            return wipes

        except ValueError:
            print("Sorry, that's not a valid number. Try again: ")

def confirmWipe():
    """Prompt user to confirm disk erasure"""

    print("WARNING!!! WRITING CHANGES TO DISK WILL RESULT IN IRRECOVERABLE DATA LOSS.")

    while True:
        try:
            reply = str(input("Are you sure you want to proceed? (Yes/No): ")).lower().strip()

            if reply == 'yes':
                return True
            elif reply == 'no':
                print("Exiting pyWype.")
                sys.exit()

        except ValueError:
            print("Sorry, that's not a valid entry. Try again: ")

def zerosToDevice():
    """Write zeros to device/partition"""

    append = appendDevice()
    num = numberOfWipes()
    confirmWipe()

    for i in range(num):
        print("Processing pass count {} of {} ... ".format(i + 1, num))
        os.system(('dd if=/dev/zero |pv --progress --time --rate --bytes| dd of={} bs=1024'.format(append))) # pv -ptrb

def randomToDevice():
    """Write random zeros and ones to device/partition"""

    append = appendDevice()
    num = numberOfWipes()
    confirmWipe()

    for i in range(num):
        print("Processing pass count {} of {} ... ".format(i + 1, num))
        os.system(('dd if=/dev/urandom |pv --progress --time --rate --bytes| dd of={} bs=1024'.format(append))) # pv -ptrb

def menu():
    """Menu prompt for use to select program option"""

    listDevices()

    while True:
        try:
            print(30 * "-", "MENU", 30 * "-")
            print("1. Overwrite device or partition with 0's \n(faster, less secure).")
            print("2. Overwrite device or partition with random 0\'s & 1\'s \n(slower, more secure).")
            print("3. Quit.")

            choice = input("Select an option (1, 2 or 3): ")

            if choice not in ('1', '2', '3'):
                raise ValueError()
            return choice

        except ValueError:
            print("Sorry, that's not a valid number. Try again: ")

def interactiveMode():
    """Display menu-driven options and run function based on selection"""

    while True:
        choice = menu()

        if choice == '3':
            sys.exit()
        elif choice == '1':
            zerosToDevice()
        elif choice == '2':
            randomToDevice()

def wipeDevice():
    """Program to Wipe drive"""

    osCheck()
    userCheck()
    interactiveMode()

if __name__ == '__main__':
    print(28 * '-', " pyWype ", 28 * '-')
    print("PYTHON DISK & PARTITION WIPING UTILITY FOR LINUX.\nTHIS WILL IRRECOVERABLY WIPE DATA FROM DRIVE.\nPROCEED WITH CAUTION.")

    wipeDevice()