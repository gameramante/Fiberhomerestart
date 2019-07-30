import requests
import sys
import time
from bs4 import BeautifulSoup
from restart import reboot

url = 'http://192.168.1.1/goform/webLogin'
login_data = {
        "User": "xxxx",
        "Passwd": "xxxxx"
    }

ses = requests.Session()

try:
    ses.post(url, data = login_data)
except requests.exceptions.ConnectionError:
    print('The router is still restarting')
    time.sleep(3)
    sys.exit(1) #exit the program

checkip = ses.get('http://192.168.1.1/state/wan_state.asp').content
soup = BeautifulSoup(checkip, 'html.parser')
ip = soup.find(id = 'wan_ip').text
print('Current ip {}'.format(ip))

of = open('ip/iprange.txt', encoding = 'utf-8').read()
if ip in of:
    print('The ip was found in the database')
else:
    print('ip not found in database')
    print('Restarting')
    reboot()