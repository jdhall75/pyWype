#!/usr/bin/env python 
#!/usr/bin/env python3 
# Refactor code
# 


from __future__ import print_function 
from builtins import input 

""" Python 2.7 &  3.4 disk wiping utility for use on Linux operating systems. RUN AS ROOT. """

import sys              # For interpreter variables & associated functions 
import os               # For operating system-dependent functions 
import re               # For regular expression parsing  

""" Define functions """

#def osCheck():
#    """ Check if OS is 'Linux' """
#    if not sys.platform.startswith('linux'):
#        print('This program was designed for Linux. Exiting.') 
#        sys.exit()

def devicesHeader():
    """ Header for attached device(s) / partition(s) """
    print(24 * "-", "ATTACHED DEVICES", 24 * "-")

def listDevices(): 
    """ List mounted device(s) / partition(s) """
    
    header = devicesHeader()

    return os.system('lsblk --nodeps --output NAME,MODEL,VENDOR,SIZE,STATE')      #lsblk -d -o NAME,MODEL,VENDOR,SIZE,STATE 

def defineDeviceHeader():
    """ Header for device(s) / partiton(s)  definition """
    print(25 * "-", "SELECT DEVICE", 25 * "-")

def defineDevice(): 
    """ Prompt user to define device or partition to wipe """
    
    devices = listDevices() 
    
    header = defineDeviceHeader()

    while True:
        try: 
            devicepartition = str(input('Enter letter of block device to be wiped, e.g. to wipe \'/dev/sdb\' enter \'b\': '))  

            if not re.match("^[a-z]$|^[a-z]\d$", devicepartition):                                       
                raise ValueError()
            return devicepartition

        except ValueError: 
            print('Sorry, that\'s not a valid device / partition. Try again.')
 
def appendDevice(): 
    """ Append user-defined device/partition to /dev/sd """
    
    letter = defineDevice()
    
    return '/dev/sd' + letter

def menu(): 
    """ Menu prompt for use to select program option """ 

    append = appendDevice()    

    while True: 
        print(30 * "-", "SELECT ACTION", 30 * "-")
        print('1. Overwrite all sectors with zeros (Faster, less secure).')
        print('2. Overwrite all sectors with random data (Slower, more secure).')
        print('3. I want to quit.') 
        choice = input('Select an option (1, 2 or 3): ')

        if choice in ('1', '2', '3'): 
            return choice 

menu()

'''
def interactiveMode(): 
    """ Display menu-driven options and return conversions. """
    while True: 
        choice = menu() 

        if choice == '3': 
            print('3')
            # sys.exit() 
        elif choice == '1': 
            print('1')
            # zerosToDevPart()
        elif choice == '2': 
            print('2')
            # randomToDevPart() 

def wipeDrive():
    """ Program to Wipe drive """ 
    
    osCheck()
    interactiveMode()
    
if __name__ == '__main__':
    print(28 * '-', " pyWype ", 28 * '-')
    print('PYTHON DISK WIPING UTILITY.\nTHIS TOOL WILL IRRECOVERABLY WIPE DATA FROM YOUR DRIVE.\nPROCEED WITH CAUTION.') 
 
    wipeDrive()
 
def numberOfWipes(): 
    """ Prompt user for number of wipes to perform """ 
    
    while True: 
        try:
            wipes = int(input('How many times do you want to wipe the disk?: '))
            
            if not wipes > 0: 
                raise ValueError()
            return wipes 

        except ValueError: 
            print('Sorry, that\'s not a valid number. Try again.')

def warningMessage(): 
    """ Warning! """
    print('WARNING!!! WRITING CHANGES TO DISK WILL RESULT IN IRRECOVERABLE DATA LOSS.') 

def confirmWipe():
    """ Prompt user to confirm disk erasure """
    
    warning = warningMessage()

    while True: 
        try: 
            reply = str(input('Are you sure you want to proceed? (Yes/No): ')).lower().strip()

            if reply == 'yes': 
                return True              
            elif reply == 'no':
                sys.exit()
                 
        except ValueError: 
            print('Sorry, that\'s not a valid entry. Try again: ') 
 
def zerosToDevPart(): 
    """ Write zeros to device/partition """
 
    append = appendDevPart() 
    num = numberOfWipes()
    confirm = confirmWipe()

    passes = 1 
    
    for int in range(num):
        print('Processing pass count {} of {} ... '.format(passes, num))
        os.system(('dd if=/dev/zero |pv --progress --time --rate --bytes| dd of={} bs=4096'.format(append))) # pv -ptrb         
        passes += 1 

def randomToDevPart():
    """ Write random zeros and ones to drive """
    
    append = appendDevPart()    
    num = numberOfWipes()
    confirm = confirmWipe()

    passes = 1 
    
    for int in range(num):
        print('Processing pass count {} of {} ...'.format(passes, num))
        os.system(('dd if=/dev/random |pv --progress --time --rate --bytes| dd of={} bs=4096'.format(append))) # pv -ptrb 
        passes += 1 


  

'''