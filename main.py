import requests
import sys
import time
from bs4 import BeautifulSoup

login_data = {
            "User": "xxxx",
            "Passwd": "xxxx"
        }

url = 'http://192.168.1.1/goform/webLogin'

def main():
    ses = requests.Session()

    try:
        ses.post(url, data = login_data)
    except requests.exceptions.ConnectionError:
        print('The router is still restarting.\n')
        print('Trying again in 10 seconds.\n')
        time.sleep(10)
        main()
    else:
        checkip = ses.get('http://192.168.1.1/state/wan_state.asp').content
        soup = BeautifulSoup(checkip, 'html.parser')
        ip = soup.find(id = 'wan_ip').text
        print('\nYour current ip is {}'.format(ip))

        of = open('ip/iprange.txt', encoding = 'utf-8').read()
        
        if ip == '0.0.0.0':
            print('Invalid IP: {}'.format(ip))
            time.sleep(2)
            main()
        elif ip in of:
            print('The ip was found in the database, quitting the program.')
            time.sleep(5)
            sys.exit(0)
        else:
            print('ip not found in database\n\n')
            print('Restarting in 3 seconds.')
            time.sleep(3)
            reboot()

def reboot():
    ses = requests.Session()

    try:
        ses.post(url, data = login_data)
    except requests.exceptions.ConnectionError:
        print('The router is still restarting\n')
        time.sleep(1)
        main()
    
    try:
        ses.get('http://192.168.1.1/goform/reboot')
    except requests.exceptions.ConnectionError:
        print('\nThe router will now restart.')
        time.sleep(5)
        main()


main()