#!python
# -*- coding: utf-8 -*-

import subprocess
import time
import omega2
from informer import Informer
from router import Router
from server import Server
from tester import Tester
from ddns import DDNS

FULL_CHECK_INTERVAL = 60 * 20  # seconds

i = Informer()
i.info('Lock and Load!')

o2 = omega2.Omega2()
r = Router('192.168.1.1', 1, lambda: open('/root/router_pwd').read())
s = Server("/root/server-run")
t = Tester(s)
d = DDNS()

o2.RGB_color(0, 0, 0)

def wifi_reconnect():
    i.notice("Restarting Wi-Fi...")
    subprocess.call("wifi", shell=True)
    i.notice("Waiting 5s for link to raise...")
    time.sleep(5)

def router_notice():
    i.notice("(¬_¬) Link failed once. Waiting 30s...")
    o2.RGB_color(0, 0, 100)
    time.sleep(30)
    wifi_reconnect()

def router_warning():
    i.notice("(ಠ_ಠ) Link failed twice. Waiting 2m...")
    o2.RGB_color(100, 1, 0) # Yellow
    time.sleep(60 * 2)
    wifi_reconnect()

def router_is_dead():
    o2.RGB_color(100, 0, 0)
    i.crytical("(ﾉ°□°)ﾉ Link is Dead. Rebooting Router.")
    if not r.soft_reboot():
        i.warning("Soft reboot failed!")
        r.hard_reboot()
    i.warning("Waiting 1m for Router to reboot...")
    time.sleep(60)
    wifi_reconnect()
    
    i.notice("Recovering sequence finished.")
    if t.ping("ya.ru", 3):
        i.notice("\(‘ ∇‘ )/ Link was raised!")
    else:
        i.notice("(╥﹏╥) Nothing helps...")

def check_router():
    if not t.ping("ya.ru", 3):
        router_notice()
        if not t.ping("google.com", 10):
            router_warning()
            if not t.ping("8.8.8.8", 10):
                router_is_dead()
                return False
            else:
                i.notice("\(‘ ∇‘ )/ Link raised by itself.")
                d.update()
        else:
            i.notice("\(‘ ∇‘ )/ Link raised by itself.")
            d.update()
    i.ok("Router")
    o2.RGB_color(0, 0, 0)
    return True

# ------------------------------------------

def server_warning():
    i.notice("(¬_¬) Server's connection fails. Waiting 1m.")
    time.sleep(60)
    i.notice("┴─┴ ノ( º _ ºノ) Maybe Router is dead? Checking this.")
    if t.ping("ya.ru", 3):
        i.notice("No, Router is OK... Is server really dead?")
    else:
        i.notice("Indeed! Router is the one to blame. Recovering sequence initiated.")
        result = "Online ^_^" if check_router() else "Still dead Т_Т"
        i.notice("Recovering sequence finished. Link status: " + result)

def server_is_dead():
    i.crytical("(ﾉ°□°)ﾉ Server is Dead. Rebooting.")
    if s.soft_reboot():
        i.warning("Waiting 3m for server to reboot...")
        time.sleep(60 * 3)
    else:
        i.crytical("¯\_(ツ)_/¯ Failed ro reboot. Giving up.")
    i.notice("Recovering sequence finished.")
    
def check_server():
    if not t.remote_ping("ya.ru", 3):
        server_warning()
        if not t.remote_ping("8.8.8.8", 10):
            server_is_dead()
            return False
        else:
            i.notice("\(‘ ∇‘ )/ Server raised by itself.")
    else:
        i.ok("Server")
        return True

while True:
    check_router()
    d.update()
    time.sleep(FULL_CHECK_INTERVAL)
