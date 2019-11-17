import requests
import sys
import time
import os
from bs4 import BeautifulSoup

login_data = {
            "User": "xxx",
            "Passwd": "xxx"
        }

def ips():
    return open('ip/iprange.txt', encoding = 'utf-8').read() #opens the ip.txt file

url = 'http://192.168.1.1/goform/webLogin'

ses = requests.Session()

def main(tries):
    try:
        print('Connecting to ONU..')
        time.sleep(0.5)
        ses.post(url, data = login_data) #login into the router
    except requests.exceptions.ConnectionError:
        clearTerminal()
        print('\nONU is still restarting.\n')
        print('Trying again in 10 seconds.')
        time.sleep(10)
        clearTerminal()
        main(tries = 0)
    else:
        clearTerminal()
        checkip = ses.get('http://192.168.1.1/state/wan_state.asp').content
        soup = BeautifulSoup(checkip, 'html.parser')
        ip = soup.find(id = 'wan_ip').text
        print('Your current ip is {}'.format(ip))
        
        if ip == '0.0.0.0':
            print('\nInvalid IP, checking ip again in 3 seconds..')
            tries += 1
            time.sleep(3)
            print('\n\nCurrent try: {} remaining tries: {}'.format(tries, 15 - tries))
            if tries >= 15:
                print('Tries excedeed the limit, forcing restart\n Tries: {}\n'.format(tries))
                tries = 0 #reset tries
                reboot()
            else:
                time.sleep(3)
                clearTerminal()
                main(tries)

        elif ip in ips():
            print('The ip was found in the database, quitting the program.')
            time.sleep(5)
            sys.exit(0)
        else:
            print('ip not found in database\n\n')
            print('Restarting in 5 seconds.')
            time.sleep(4)
            clearTerminal()
            reboot()

def reboot():
    try:
        print('Connecting to ONU...')
        ses.post(url, data = login_data) #login into the router
    except requests.exceptions.ConnectionError:
        clearTerminal()
        print('The router is still restarting, trying again in 5 seconds')
        time.sleep(4)
        main(tries = 0)
    
    try:
        ses.get('http://192.168.1.1/goform/reboot')
    except requests.exceptions.ConnectionError:
        print('ONU is now restarting.')
        time.sleep(2)
        clearTerminal()
        main(tries = 0)

def clearTerminal():
    if sys.platform.startswith('win32'):
        return os.system('cls')
    elif sys.platform.startswith('linux'):
        return os.system('clear')
    else:
        return os.system('clear')

main(tries = 0)
