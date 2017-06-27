import subprocess
import time
import omega2

o2 = omega2.Omega2()

def ping(host, waiting_time):
    try:
        cmd = ' '.join(["ping", host, "-c", "1", "-W", str(waiting_time)])
        print('[CALL] ' + cmd)
        ping_ret = str(subprocess.check_output(cmd, shell=True))
        return bool(ping_ret.split("packets transmitted,", 1)[-1].split(" received,", 1)[0])
    except subprocess.CalledProcessError:
        return False

def router_notice():
    print("Router Notice")
    o2.RGB_color(0, 0, 100)
    time.sleep(30)
    subprocess.call("wifi", shell=True)
    time.sleep(10)

def router_warning():
    print("Router Warning")
    o2.RGB_color(100, 1, 0) # Yellow
    time.sleep(120)
    subprocess.call("wifi", shell=True)
    time.sleep(20)

def router_is_dead():
    o2.RGB_color(100, 0, 0)
    print("Router is Dead")

def check_router():
    if not ping("ya.ru", 1):
        router_notice()

        if not ping("google.com", 10):
            router_warning()

            if not ping("8.8.8.8", 10):
                router_is_dead()

                return False
    o2.RGB_color(0, 0, 0)
    print("Router OK")
    return True

def server_ping(host, waiting_time):
    try:
        cmd = ' '.join(["/root/server-run", "ping", host, "-c", "1", "-W", str(waiting_time)])
        print('[REMOTE CALL] ' + cmd)
        ret = str(subprocess.check_output(cmd, shell=True))
        return bool(ret.split("packets transmitted,", 1)[-1].split(" received,", 1)[0])
    except subprocess.CalledProcessError:
        return False

def check_server():
    if not server_ping("ya.ru", 1):
        print("Server Warning")
        time.sleep(120)
        if not server_ping("8.8.8.8", 10):
            print("Server is Dead. Rebooting")
            try:
                subprocess.call("/root/server-run sudo reboot", shell=True)
            except subprocess.CalledProcessError:
                pass
            time.sleep(120)
    else:
        print("Server OK")

while True:
    time.sleep(5)
    check_router()

    time.sleep(5)
    check_server()

