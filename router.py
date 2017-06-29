import time
import telnetlib
import omega2
from informer import Informer

class Router(object):
    def __init__(self, ip, relay_pin, pwd_func):
        self.i = Informer('Router')
        self.relay_pin = relay_pin
        self.ip = ip
        try:
            self.o2 = omega2.Omega2()
        except:
            self.o2 = None
        self.get_pwd = pwd_func

    def _check_output(self, tn, cmd):
        self.i.info("Sending '" + cmd + "'")
        tn.write(cmd + '\n')
        tn.read_until('> ', 10)  # Inpit
        ret = tn.read_until('> ', 10)  # Output
        if ret:
            ret = ret.split('\n', 1)
            if len(ret) > 1:
                return ret[1]

    def soft_reboot(self):
        self.i.warning('Soft reboot requested!')
        try:
            tn = telnetlib.Telnet(self.ip, timeout=10)
            self.i.info('Connected via telnet')

            tn.read_until('Login: ', 10)
            tn.write('admin\n')
            tn.read_until('Password: ', 10)
            tn.write(self.get_pwd())

            module = tn.read_until('> ', 10)
            if module:
                self.i.info('Logged in: ' + module.split('\n', 1)[1])
                tn.read_very_eager()

                tn.write('system reboot\n')
                self.i.crytical('Rebooting!')
                return True
            return False
        except Exception as e:
            self.i.warning("Exception: " + str(e))
            return False

    def hard_reboot(self):
        self.i.warning('Hard reboot requested! Powering down.')
        self.o2.gpio_set(self.relay_pin, 0)
        time.sleep(5)
        self.o2.gpio_set(self.relay_pin, 1)
        self.i.crytical('Powered up. Router is rebooting (hope so)!')
