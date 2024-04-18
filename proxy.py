import requests

proxies = {"http":"" ,
           "https": ""}
a=requests.get("https://api.ipify.org/?format=json",  proxies=proxies)
print(a.json())