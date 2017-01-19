#!/usr/bin/env python3
from bs4 import BeautifulSoup
import requests
from datetime import datetime
import json

# create an access token from pushbullet's My Account page
pb_accesstokens = ['o.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx']

url = "https://console.online.net/en/order/server_limited"
# url = "https://console.online.net/en/order/server"
html = requests.get(url).text
soup = BeautifulSoup(html, "lxml")
rows = soup.find_all("tr")

servers = []
attrs = ("name", "cpu", "mem", "disk", "net", "avail", "price")
for row in rows:
    cols = row.find_all("td")
    # empty lists evaluate to false
    if cols:
        servers.append({name:cols[idx].text for idx, name in enumerate(attrs)})

msg = ""
for server in servers:
    server["avail"] = server["avail"].strip()
    if "XC" in server["name"] and not "SSD" in server["disk"]:
        if server["avail"] != "back order" and "victim" not in server["avail"]:
            msg += "{} is available for {} with {} left\n".format(server["name"], server["price"], server["avail"])

if msg:
    msg += "happened at {}\n".format(datetime.now())
    msg += url
    print("sending message:", msg)

    for token in pb_accesstokens:
        headers = {"Content-Type": "application/json", "Access-Token": token}

        postdata = {}
        postdata["title"] = "Online.net notification"
        postdata["body"] = msg
        postdata["type"] = "note"
        postdata = json.dumps(postdata)

        notifreq = requests.post("https://api.pushbullet.com/v2/pushes", data=postdata, headers=headers)

    print(notifreq.text)

else:
    print("nothing at {}".format(datetime.now()))
