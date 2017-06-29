import subprocess
import time
import omega2
from informer import Informer
from router import Router
from server import Server
from tester import Tester

i = Informer()
i.info('Lock and Load!')

o2 = omega2.Omega2()
r = Router('192.168.1.1', 1, lambda: open('/root/router_pwd').read())
s = Server("/root/server-run")
t = Tester(s)

def wifi_reconnect():
    subprocess.call("wifi", shell=True)
    i.notice("Waiting 10s for link to raise...")
    time.sleep(10)

def router_notice():
    i.notice("Router's connection failed once. Waiting 30s...")
    o2.RGB_color(0, 0, 100)
    time.sleep(30)
    wifi_reconnect()

def router_warning():
    i.notice("Router 's connection failed twice. Waiting 2m...")
    o2.RGB_color(100, 1, 0) # Yellow
    time.sleep(120)
    wifi_reconnect()

def router_is_dead():
    o2.RGB_color(100, 0, 0)
    i.warning("Connection is Dead. Trying to reboot...")
    if not r.soft_reboot():
        r.hard_reboot()
    i.warning("Waiting 1m for router to reboot...")
    time.sleep(60)
    wifi_reconnect()

def check_router():
    if not t.ping("ya.ru", 1):
        router_notice()
        if not t.ping("google.com", 10):
            router_warning()
            if not t.ping("8.8.8.8", 10):
                router_is_dead()
                return False
    o2.RGB_color(0, 0, 0)
    i.info("Router OK")
    return True

# ------------------------------------------

def server_warning():
    i.notice("Server's connection fails. Waiting 1m.")
    time.sleep(60)
    i.notice("Maybe router is dead? Checking this.")
    check_router()

def server_is_dead():
    i.warning("Server's connection still fails. Trying to reboot.")
    if s.soft_reboot():
        i.warning("Waiting 3m for server to reboot...")
        time.sleep(60 * 3)
    else:
        i.crytical("Server is badly dead and needs a hard reset.")

def check_server():
    if not t.remote_ping("ya.ru", 1):
        server_warning()
        if not t.remote_ping("8.8.8.8", 10):
            server_is_dead()
            return False
    else:
        i.info("Server OK")
        return True

while True:
    time.sleep(5)
    if check_router():
        time.sleep(5)
        check_server()
