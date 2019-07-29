import requests
import time
import sys

url = 'http://192.168.1.1/goform/webLogin'

def reboot():
    
    login_data = {
        "User": "xxx",
        "Passwd": "xxx"
    }

    ses = requests.Session()

    try:
        ses.post(url, data = login_data)
    except requests.exceptions.ConnectionError:
        print('The router is still restarting')
        time.sleep(3)
        sys.exit(0) #exit the program
    
    try:
        ses.get('http://192.168.1.1/goform/reboot')
    except requests.exceptions.ConnectionError:
        print('The router is now restarting.')
        time.sleep(5)
        sys.exit(0)

reboot()