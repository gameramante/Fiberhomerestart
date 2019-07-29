import requests


url = 'http://192.168.1.1/goform/webLogin'


login_data = {
    "User": "xxxx",
    "Passwd": "xxxx"
}
ses = requests.Session()

login = ses.post(url, data = login_data)
reboot = ses.get('http://192.168.1.1/goform/reboot')
