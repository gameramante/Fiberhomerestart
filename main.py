import requests
import sys
import time
import os
from bs4 import BeautifulSoup

login_data = {
            "User": "***",
            "Passwd": "***"
        }

of = open('ip/iprange.txt', encoding = 'utf-8').read() #open the ip.txt file

url = 'http://192.168.1.1/goform/webLogin'

ses = requests.Session()

def main(tries):
    try:
        print('Connecting to ONU..')
        time.sleep(0.5)
        ses.post(url, data = login_data) #login into the router
    except requests.exceptions.ConnectionError:
        os.system('cls')
        print('\nONU is still restarting.\n')
        print('Trying again in 10 seconds.')
        time.sleep(10)
        os.system('cls')
        main(tries = 0)
    else:
        os.system('cls')
        checkip = ses.get('http://192.168.1.1/state/wan_state.asp').content
        soup = BeautifulSoup(checkip, 'html.parser')
        ip = soup.find(id = 'wan_ip').text
        print('Your current ip is {}'.format(ip))
        
        if ip == '0.0.0.0':
            print('\nInvalid IP, checking ip again in 3 seconds..')
            tries += 1
            print('\n\nCurrent try: {} remaining tries: {}'.format(tries, 15 - tries))
            if tries >= 15:
                print('Tries excedeed the limit, forcing restart\n Tries: {}\n'.format(tries))
                tries = 0 #reset tries
                reboot()
            else:
                time.sleep(3)
                os.system('cls')
                main(tries)

        elif ip in of:
            print('The ip was found in the database, quitting the program.')
            time.sleep(5)
            sys.exit(0)
        else:
            print('ip not found in database\n\n')
            print('Restarting in 5 seconds.')
            time.sleep(4)
            os.system('cls')
            reboot()

def reboot():
    try:
        print('Connecting to ONU...')
        ses.post(url, data = login_data) #login into the router
    except requests.exceptions.ConnectionError:
        os.system('cls')
        print('The router is still restarting, trying again in 5 seconds\n')
        time.sleep(4)
        main(tries = 0)
    
    try:
        ses.get('http://192.168.1.1/goform/reboot')
    except requests.exceptions.ConnectionError:
        print('\nONU is now restarting.')
        time.sleep(2)
        os.system('cls')
        main(tries = 0)

main(tries = 0)