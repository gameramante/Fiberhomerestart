import requests
import sys
import time
import os
from bs4 import BeautifulSoup

login_data = {
            "User": "xxx",
            "Passwd": "xxx"
        }

url = 'http://192.168.1.1/goform/webLogin'

def main():
    ses = requests.Session()

    try:
        print('Trying to connect to ONU...')
        time.sleep(2)
        ses.post(url, data = login_data) #login into the router
    except requests.exceptions.ConnectionError:
        print('\n\nONU is still restarting.\n')
        print('Trying again in 10 seconds.')
        time.sleep(10)
        os.system('cls')
        main()
    else:
        os.system('cls')
        checkip = ses.get('http://192.168.1.1/state/wan_state.asp').content
        soup = BeautifulSoup(checkip, 'html.parser')
        ip = soup.find(id = 'wan_ip').text
        print('Your current ip is {}'.format(ip))

        of = open('ip/iprange.txt', encoding = 'utf-8').read()
        
        if ip == '0.0.0.0':
            print('\n\nInvalid IP, restarting script in 10 seconds')
            time.sleep(10)
            os.system('cls')
            main()
        elif ip in of:
            print('The ip was found in the database, quitting the program.')
            time.sleep(5)
            sys.exit(0)
        else:
            print('ip not found in database\n\n')
            print('Restarting in 3 seconds.')
            time.sleep(3)
            os.system('cls')
            reboot()

def reboot():
    ses = requests.Session()

    try:
        print('Connecting to ONU...')
        ses.post(url, data = login_data)
    except requests.exceptions.ConnectionError:
        os.system('cls')
        print('The router is still restarting.\n')
        time.sleep(3)
        main()
    
    try:
        ses.get('http://192.168.1.1/goform/reboot')
    except requests.exceptions.ConnectionError:
        print('\nRestarting ONU.')
        time.sleep(5)
        os.system('cls')
        main()

main()