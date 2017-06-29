import subprocess
import time
import omega2
from informer import Informer
from router import Router
from server import Server
from tester import Tester


o2 = omega2.Omega2()
i = Informer()
r = Router('192.168.1.1', 1, lambda: open('/root/router_pwd').read())
s = Server("/root/server-run")
t = Tester(s)


def router_notice():
    i.notice("Router does not respond once")
    o2.RGB_color(0, 0, 100)
    time.sleep(30)
    subprocess.call("wifi", shell=True)
    time.sleep(10)

def router_warning():
    i.notice("Router does not respond twice")
    o2.RGB_color(100, 1, 0) # Yellow
    time.sleep(120)
    subprocess.call("wifi", shell=True)
    time.sleep(20)

def router_is_dead():
    o2.RGB_color(100, 0, 0)
    i.warning("Router is Dead. Trying to reboot.")
    if not r.soft_reboot():
        r.hard_reboot()
    time.sleep(120)

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
    i.notice("Server's connection fails")
    time.sleep(60)
    check_router()

def server_is_dead():
    i.warning("Server's connection still fails. Trying to reboot.")
    s.soft_reboot()
    time.sleep(240)

def check_server():
    if not t.remote_ping("ya.ru", 1):
        server_warning()
        if not t.remote_ping("8.8.8.8", 10):
            server_is_dead()
    else:
        i.info("Server OK")

while True:
    time.sleep(5)
    check_router()

    time.sleep(5)
    check_server()

