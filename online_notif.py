#!/usr/bin/env python3
from bs4 import BeautifulSoup
import requests
from datetime import datetime

url = "https://console.online.net/en/order/server_limited"
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
    # the avail cells have \n's everywhere
    server["avail"] = server["avail"].strip()
    if server["avail"] != "back order":
        msg += "{} is available for {} with {} left\n".format(server["name"], server["price"], server["avail"])

if msg:
    msg += "happened at {}".format(datetime.now())
    print("sending message:", msg)

    postdata = {}
    postdata["apikey"] = "putemhere"
    postdata["application"] = "onlinenet notif"
    postdata["event"] = "Online.net server in stock"
    postdata["description"] = msg
    postdata["priority"] = 2
    postdata["url"] = url
    notifreq = requests.post("https://www.notifymyandroid.com/publicapi/notify", data=postdata)
    print(notifreq.text)
