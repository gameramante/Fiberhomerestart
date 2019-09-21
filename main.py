import requests
import sys
import time
import os
from bs4 import BeautifulSoup

login_data = {
            "User": "***",
            "Passwd": "***"
        }

of = open('ip/iprange.txt', encoding = 'utf-8').read()

url = 'http://192.168.1.1/goform/webLogin'

ses = requests.Session()

def main():
    try:
        print('Trying to connect to ONU...')
        time.sleep(1)
        ses.post(url, data = login_data) #login into the router
    except requests.exceptions.ConnectionError:
        os.system('cls')
        print('\n\nONU is still restarting.\n')
        print('Trying again in 15 seconds.')
        time.sleep(15)
        os.system('cls')
        main()
    else:
        os.system('cls')
        checkip = ses.get('http://192.168.1.1/state/wan_state.asp').content
        soup = BeautifulSoup(checkip, 'html.parser')
        ip = soup.find(id = 'wan_ip').text
        print('Your current ip is {}'.format(ip))
        
        if ip == '0.0.0.0':
            print('\nInvalid IP, checking ip again in 15 seconds..')
            time.sleep(15)
            os.system('cls')
            main()

        elif ip in of:
            print('The ip was found in the database, quitting the program.')
            time.sleep(5)
            sys.exit(0)
        else:
            print('ip not found in database\n\n')
            print('Restarting in 5 seconds.')
            time.sleep(5)
            os.system('cls')
            reboot()

def reboot():
    try:
        print('Connecting to ONU...')
        ses.post(url, data = login_data) #login into the router
    except requests.exceptions.ConnectionError:
        os.system('cls')
        print('The router is still restarting, trying again in 5 seconds\n')
        time.sleep(5)
        main()
    
    try:
        ses.get('http://192.168.1.1/goform/reboot')
    except requests.exceptions.ConnectionError:
        print('\nONU is not restarting.')
        time.sleep(3)
        os.system('cls')
        main()

main()