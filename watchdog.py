import subprocess
import time
import omega2
import telnetlib

def router_soft_reset():
	try:
		tn = telnetlib.Telnet('192.168.1.1', timeout=10)
		print '[INFO] Connected!'
		
	
		def check_output(cmd):
		    print "[INFO] Sending '" + cmd + "'"
		    tn.write(cmd + '\n')
		    tn.read_until('> ', 10)  # Inpit
		    r = tn.read_until('> ', 10)  # Output
		    if r:
		        r = r.split('\n', 1)
		        if len(r) > 1:
		            return r[1]
	
	
		def tn_exit():
		    print '[INFO] Exitting...'
		    tn.write('exit\n')
		    tn.close()
		
		tn.read_until('Login: ', 10)
		tn.write('admin\n')
		tn.read_until('Password: ', 10)
		tn.write(open('/root/router_pwd').read())
		
		module = tn.read_until('> ', 10)
		if module:
		    print '[INFO] Logged in: ' + module.split('\n', 1)[1]
		    tn.read_very_eager()
		
		    print '[INFO] Rebooting!'
		    tn.write('system reboot\n')
		    return True
		return False
	except:
		return False

o2 = omega2.Omega2()


def router_hard_reset():
	o2.gpio_set(1, 0)
	time.sleep(5)
	o2.gpio_set(1, 1)


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

