import subprocess
from informer import Informer

class Server(object):
    def __init__(self, remote_run_path):
        self.remote_run_path = remote_run_path
        self.i = Informer('Server')

    def soft_reboot(self):
        self.i.warning('Soft reboot requested!')
        try:
            subprocess.call(self.remote_run_path + " sudo reboot", shell=True)
            return True
        except subprocess.CalledProcessError:
            self.i.crytical('Reboot failed!')
            return False
