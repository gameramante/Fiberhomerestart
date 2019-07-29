import requests

url = 'http://192.168.1.1/goform/webLogin'

def reboot():
    
    login_data = {
        "User": "xxxxx",
        "Passwd": "xxxxx"
    }

    ses = requests.Session()

    try:
        ses.post(url, data = login_data)
    except requests.exceptions.ConnectionError:
        print('The router is still restarting')
    
    try:
        ses.get('http://192.168.1.1/goform/reboot')
    except requests.exceptions.ConnectionError:
        print('The router is now restarting.')

reboot()