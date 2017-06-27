import telnetlib

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

tn.read_until("Login: ", 10)
tn.write("admin\n")
tn.read_until("Password: ", 10)
tn.write("\n")  # You have not seen this.

module = tn.read_until('> ', 10)
if module:
    print '[INFO] Logged in: ' + module.split('\n', 1)[1]
    tn.read_very_eager()

    print '[INFO] Rebooting!'
    tn.write('system reboot\n')
